import streamlit as st
import boto3
import cv2
import numpy as np

# Title
st.title("🚀 EC2 Launch with Hand Gestures (No MediaPipe)")

# AWS EC2 client
ec2 = boto3.client("ec2")

# Start camera
cap = cv2.VideoCapture(0)

st.write("✋ Show **1 finger** to launch EC2 instance")

launch_triggered = False

# Stream video feed
frame_placeholder = st.empty()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        st.error("❌ Camera not accessible")
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)

    # Define ROI (Region of Interest) for the hand
    roi = frame[100:300, 100:300]
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)

    # Convert to HSV and threshold for skin color
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Blur and threshold
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        cnt_area = cv2.contourArea(cnt)

        if cnt_area > 2000:
            # Convexity defects to detect fingers
            hull_indices = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull_indices)

            if defects is not None:
                finger_count = 0
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    a = np.linalg.norm(np.array(end) - np.array(start))
                    b = np.linalg.norm(np.array(far) - np.array(start))
                    c = np.linalg.norm(np.array(end) - np.array(far))
                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

                    if angle <= np.pi / 2:
                        finger_count += 1

                # Fingers count = defects + 1
                fingers_up = finger_count + 1

                cv2.putText(frame, f"Fingers: {fingers_up}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if fingers_up == 1 and not launch_triggered:
                    st.success("🖐 Detected gesture — launching EC2 instance...")
                    try:
                        response = ec2.run_instances(
                            ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2
                            InstanceType='t2.micro',
                            MinCount=1,
                            MaxCount=1
                        )
                        instance_id = response['Instances'][0]['InstanceId']
                        st.write(f"✅ Instance Launched: {instance_id}")
                        launch_triggered = True
                    except Exception as e:
                        st.error(f"Error: {e}")

    frame_placeholder.image(frame, channels="BGR")

cap.release()

