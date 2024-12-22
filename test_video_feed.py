import cv2
import math
import time
import mediapipe as mp
import os
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

############################
# MODEL PATH
############################
directory_path = os.path.dirname(__file__)
MODEL_PATH = os.path.join(directory_path, 'pose_landmarker_lite.task')

############################
# DRAWING UTILS
############################
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

############################
# HELPERS FOR POSTURE METRICS
############################
def angle_2d(a, b, c):
    # Same as before...
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    dot_prod = ab[0]*cb[0] + ab[1]*cb[1]
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)
    if mag_ab < 1e-6 or mag_cb < 1e-6:
        return None  
    cos_angle = dot_prod / (mag_ab * mag_cb)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    return math.degrees(math.acos(cos_angle))

def vertical_difference(pt1, pt2, image_height):
    return abs(pt1.y - pt2.y) * image_height

def horizontal_offset(pt_shoulder, pt_hip, image_width):
    return (pt_shoulder.x - pt_hip.x) * image_width

############################
# GLOBALS FOR CALLBACK
############################
g_posture_metrics = {
    "forward_head_angle": None,
    "shoulder_height_diff": None,
    "shoulder_hip_offset": None
}

g_pose_result = None  # We'll store the last PoseLandmarkerResult here.

############################
# LANDMARK DRAWING FUNCTION
############################
def draw_landmarks_on_image(frame, pose_result):
    """
    Draw the pose landmarks + connections on 'frame' (BGR image)
    using Mediapipe's drawing_utils.
    """
    if not pose_result or not pose_result.pose_landmarks:
        return frame  # Nothing to draw
    from mediapipe.framework.formats import landmark_pb2
    # We'll loop over each detected pose. Usually it's 1 for single-person detection.
    for pose_landmarks in pose_result.pose_landmarks:
        # Convert to a NormalizedLandmarkList proto for drawing_utils
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(
                x=lmk.x, y=lmk.y, z=lmk.z, visibility=lmk.visibility
            ) 
            for lmk in pose_landmarks
        ])

        # Draw the landmarks and connections
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=pose_landmarks_proto,
            connections=mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 255), thickness=2, circle_radius=2
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(0, 255, 0), thickness=2, circle_radius=2
            ),
        )
    return frame

############################
# CALLBACK
############################
def analyze_posture(result: vision.PoseLandmarkerResult,
                    output_image: mp.Image,
                    timestamp_ms: int):
    """
    Called each time the PoseLandmarker has a new result.
    We compute posture metrics and store them, plus store 'result' in g_pose_result 
    so we can draw landmarks in the main loop.
    """
    global g_posture_metrics, g_pose_result
    g_pose_result = result  # store the last full result for drawing

    # Basic posture data defaults
    posture_data = {
        "forward_head_angle": None,
        "shoulder_height_diff": None,
        "shoulder_hip_offset": None,
    }

    if not result.pose_landmarks:
        g_posture_metrics = posture_data
        return

    landmarks = result.pose_landmarks[0]  # single person
    h, w = output_image.numpy_view().shape[:2]

    # Indices
    L_EAR, R_EAR = 7, 8
    L_SHOULDER, R_SHOULDER = 11, 12
    L_HIP, R_HIP = 23, 24

    needed_idx = [L_EAR, R_EAR, L_SHOULDER, R_SHOULDER, L_HIP, R_HIP]
    if any(idx >= len(landmarks) for idx in needed_idx):
        g_posture_metrics = posture_data
        return

    ear_left = landmarks[L_EAR]
    shoulder_left = landmarks[L_SHOULDER]
    hip_left = landmarks[L_HIP]
    # Forward head angle
    e = (ear_left.x, ear_left.y, ear_left.z)
    s = (shoulder_left.x, shoulder_left.y, shoulder_left.z)
    h_ = (hip_left.x, hip_left.y, hip_left.z)
    fwd_head_angle = angle_2d(e, s, h_)
    posture_data["forward_head_angle"] = fwd_head_angle

    # Shoulder height diff
    shoulder_right = landmarks[R_SHOULDER]
    sh_height_diff = vertical_difference(shoulder_left, shoulder_right, h)
    posture_data["shoulder_height_diff"] = sh_height_diff

    # Shoulder-hip offset
    sh_hip_off = horizontal_offset(shoulder_left, hip_left, w)
    posture_data["shoulder_hip_offset"] = sh_hip_off

    g_posture_metrics = posture_data

############################
# MAIN LOOP
############################
def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera.")
        return

    # Create a PoseLandmarker in LIVE_STREAM mode
    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=analyze_posture
    )
    landmarker = PoseLandmarker.create_from_options(options)

    while True:
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            time.sleep(0.01)
            continue

        # Wrap frame in an MP Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame
        )

        # Run detection
        landmarker.detect_async(
            mp_image,
            timestamp_ms=int(time.time() * 1000)
        )

        # ======================
        # DRAW LANDMARKS
        # ======================
        # If we have a pose result, draw it on the BGR frame
        global g_pose_result
        if g_pose_result is not None:
            frame = draw_landmarks_on_image(frame, g_pose_result)

        # ======================
        # OVERLAY POSTURE DATA
        # ======================
        fwd_angle = g_posture_metrics.get("forward_head_angle", None)
        if fwd_angle is not None:
            text = f"Forward Head Angle (Ear-Shoulder-Hip): {fwd_angle:.1f}°"
            cv2.putText(
                frame, text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )

        sh_diff = g_posture_metrics.get("shoulder_height_diff", None)
        if sh_diff is not None:
            text = f"Shoulder Height Diff: {sh_diff:.1f} px"
            cv2.putText(
                frame, text, (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2
            )

        sh_hip_off = g_posture_metrics.get("shoulder_hip_offset", None)
        if sh_hip_off is not None:
            text = f"Shoulder-Hip Offset: {sh_hip_off:.1f} px"
            cv2.putText(
                frame, text, (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2
            )

        # Show the frame
        cv2.imshow("Muscle Imbalance / Posture Analysis with Landmarks", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
