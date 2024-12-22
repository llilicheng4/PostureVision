# **PostureVision: AI-Powered Muscle Imbalance Detector** \u267B

## **Inspiration** \u2728
Many of us spend long hours sitting at desks, staring at screens, and adopting less-than-ideal postures—leading to potential neck pain, rounded shoulders, and other musculoskeletal issues. Our team wanted to create an accessible tool that **scans for potential muscle imbalances** in real time, helping users become more aware of posture pitfalls and take corrective steps before bigger problems arise. \uD83E\uDEE0

## **What It Does** \uD83D\uDCC8
**PostureVision** uses a **webcam** feed to:
1. **Capture Real-Time Video** from your PC or laptop camera. \uD83D\uDCF7  
2. **Apply Pose Estimation** (via MediaPipe Tasks) to pinpoint key landmarks: ears, shoulders, hips, etc. \uD83D\uDC68\u200D\uD83C\uDF93  
3. **Calculate Posture Metrics**:
   - **Forward head posture** (ear–shoulder–hip angle) \uD83E\uDDD0  
   - **Shoulder height difference** (left vs. right) \u2B06\u2B07  
   - **Rounded shoulders** (how far forward shoulders drift relative to hips) \u267F  
4. **Provide Instant Feedback** with on-screen **visualizations**: A skeleton overlay draws each landmark and posture metrics (angles, offsets) in real time. \uD83E\uDDE0  
5. **Suggest Possible Imbalances** based on physiotherapy guidelines—e.g., angles below certain thresholds or large side-to-side differences. \u2695\uFE0F

## **How We Built It** \uD83E\uDDE9
1. **OpenCV**: For live video capture and image display. \uD83D\uDCF9  
2. **MediaPipe Tasks** (Pose Landmarker): For accurate real-time pose detection with minimal overhead. \uD83E\uDD16  
3. **Python**: The main glue language tying everything together, including angle calculations, measuring offsets, and rendering the final results. \uD83D\uDCBB  
4. **NumPy**: For numerical operations, coordinate transformations, and optional data logging. \u2795\u2139  
5. **Hackathon Collaboration**: We used GitHub for version control and Slack/Discord for quick communication to coordinate sprints. \uD83D\uDCE2

## **Challenges We Ran Into** \u26A0\uFE0F
- **Real-Time Performance**: Running pose estimation on each frame can be heavy. We tackled this by trying smaller models. \u231B  
- **Reliable Landmark Detection** in varied conditions. We tested multiple lighting setups and vantage points. \uD83E\uDDE1  
- **Defining Healthy vs. Unhealthy Ranges**: Translating clinical guidelines into angles and offsets is tricky. We adopted approximate thresholds (e.g., <160° forward head angle as “at risk”) based on physiotherapy references. \uD83D\uDCD6

## **Accomplishments That We’re Proud Of** \uD83C\uDFC6
- **Accurate, Real-Time Posture Analysis**: Even on basic hardware, the system displays postural metrics with minimal lag. \u23F3  
- **Clean, Visual Overlay**: A skeleton drawn over the user feed helps them immediately see which areas might be misaligned. \uD83D\uDD8C\uFE0F

## **What We Learned** \uD83D\uDCDA
- **Power of MediaPipe**: Easy extraction of landmarks for custom calculations. \uD83C\uDF1F  
- **Importance of Testing Across Different People**: Everyone’s skeletal and muscular system is unique, so we tested angles/offsets on multiple participants. \uD83D\uDCAA  
- **Researched Intensively**: Read multiple papers on this topic \uD83D\uDCD8

## **What’s Next for PostureVision** \uD83D\uDE80
1. **Extended Collaborations**: Work more closely with **physical therapists and doctors** to refine our detection methods, validate thresholds, and enhance accuracy in real-world clinical settings. \uD83D\uDC68\u200D\u2695\uFE0F  
2. **Expanded Mobility Library**: Automatically present evidence-based **light exercises** and stretches—personalized for each user’s posture data—to help them correct imbalances. \uD83D\uDCAA  
3. **User Profiles & Logging**: Store session data over time, show progress graphs, and detect trends in posture improvement or regression. \u23F0  
4. **Personalized Alerts**: Notify the user (via on-screen prompts or phone notifications) when posture drifts outside healthy ranges. \uD83D\uDCF1  
5. **Mobile or Web Integration**: Wrap the tool into an Electron app or a cross-platform mobile framework for broader reach. \uD83D\uDCBB  
