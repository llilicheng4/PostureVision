# **PostureVision: AI-Powered Muscle Imbalance Detector**

## **Inspiration**
Many of us spend long hours sitting at desks, staring at screens, and adopting less-than-ideal postures—leading to potential neck pain, rounded shoulders, and other musculoskeletal issues. Our team wanted to create an accessible tool that **scans for potential muscle imbalances** in real time, helping users become more aware of posture pitfalls and take corrective steps before bigger problems arise.

## **What It Does**
**PostureVision** uses a **webcam** feed to:
1. **Capture Real-Time Video** from your PC or laptop camera.  
2. **Apply Pose Estimation** (via MediaPipe Tasks) to pinpoint key landmarks: ears, shoulders, hips, etc.  
3. **Calculate Posture Metrics**:
   - **Forward head posture** (ear–shoulder–hip angle),  
   - **Shoulder height difference** (left vs. right),  
   - **Rounded shoulders** (how far forward shoulders drift relative to hips).  
4. **Provide Instant Feedback** with on-screen **visualizations**: A skeleton overlay draws each landmark and posture metrics (angles, offsets) in real time.  
5. **Suggest Possible Imbalances** based on physiotherapy guidelines—e.g., angles below certain thresholds or large side-to-side differences.  

## **How We Built It**
1. **OpenCV**: For live video capture and image display.  
2. **MediaPipe Tasks** (Pose Landmarker): For accurate real-time pose detection with minimal overhead.  
3. **Python**: The main glue language tying everything together, including angle calculations, measuring offsets, and rendering the final results.  
4. **NumPy**: For numerical operations, coordinate transformations, and optional data logging.  
5. **Hackathon Collaboration**: We used GitHub for version control and Slack/Discord for quick communication to coordinate sprints.

## **Challenges We Ran Into**
- **Real-Time Performance**: Running pose estimation on each frame can be heavy. We tackled this by trying smaller models.
- **Reliable Landmark Detection** in varied conditions. We tested multiple lighting setups and vantage points.  
- **Defining Healthy vs. Unhealthy Ranges**: Translating clinical guidelines into angles and offsets is tricky. We adopted approximate thresholds (e.g., <160° forward head angle as “at risk”) based on physiotherapy references.

## **Accomplishments That We’re Proud Of**
- **Accurate, Real-Time Posture Analysis**: Even on basic hardware, the system displays postural metrics with minimal lag.  
- **Clean, Visual Overlay**: A skeleton drawn over the user feed helps them immediately see which areas might be misaligned.  

## **What We Learned**
- **Power of MediaPipe**: Easy extraction of landmarks for custom calculations.  
- **Importance of Testing Across Different People**: Everyone’s skeletal and muscular system is unique, so we tested angles/offsets on multiple participants.  
- **Researched Intensively**: Read multiple papers on this topic

## **What’s Next for PostureVision**
1. **Extended Collaborations**: Work more closely with **physical therapists and doctors** to refine our detection methods, validate thresholds, and enhance accuracy in real-world clinical settings.  
2. **Expanded Mobility Library**: Automatically present evidence-based **light exercises** and stretches—personalized for each user’s posture data—to help them correct imbalances.  
3. **User Profiles & Logging**: Store session data over time, show progress graphs, and detect trends in posture improvement or regression.  
4. **Personalized Alerts**: Notify the user (via on-screen prompts or phone notifications) when posture drifts outside healthy ranges.  
5. **Mobile or Web Integration**: Wrap the tool into an Electron app or a cross-platform mobile framework for broader reach.
