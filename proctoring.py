# proctoring.py
import cv2
import time
import threading
import numpy as np
from datetime import datetime
import winsound
from facial_detections import detectFace
from blink_detection import isBlinking
from mouth_tracking import mouthTrack
from object_detection import detectObject
from eye_tracker import gazeDetection
from head_pose_estimation import head_pose_detection
from telegram_alert import send_telegram_alert

# ------------------ Global Variables ------------------
data_record = []
stop_flag = False

frequency = 2500
duration = 1000

# ------------------ Helper Functions ------------------
def faceCount_detection(faceCount, frame):
    if faceCount > 1:
        winsound.Beep(frequency, duration)
        save_and_alert(frame, "Multiple faces detected")
        return "Multiple faces detected"
    elif faceCount == 0:
        winsound.Beep(frequency, duration)
        return "No face detected"
    else:
        return "Face OK"

def save_and_alert(frame, alert_message):
    """
    Capture frame and send Telegram alert
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"suspicious_{timestamp}.jpg"
    cv2.imwrite(image_path, frame)
    # create a thread to send the alert so it doesn't block main loop
    threading.Thread(target=send_telegram_alert, args=(image_path, alert_message)).start()

# ------------------ Main Proctoring Algorithm ------------------
def proctoringAlgo():
    global stop_flag, data_record
    stop_flag = False
    
    # Initialize camera
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    while not stop_flag:
        ret, frame = cam.read()

        if not ret:
            print("Camera frame not captured properly")
            continue

        frame = np.array(frame, dtype=np.uint8)

        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        record = []

        current_time = datetime.now().strftime("%H:%M:%S.%f")
        print("Current Time is:", current_time)
        record.append(current_time)

        # ---- Face Detection ----
        # unpack only what we need, handle variable return length if needed
        face_result = detectFace(frame)
        if len(face_result) == 3:
            faceCount, faces, frame = face_result
        else:
            faceCount, faces = face_result
            # failing gracefully if frame isn't returned

        record.append(faceCount_detection(faceCount, frame))

        if faceCount == 1:
            try:
                # ---- Blink Detection ----
                blinkStatus = isBlinking(faces, frame)
                status_text = blinkStatus[2] if len(blinkStatus) > 2 else str(blinkStatus)
                record.append(status_text)
                if status_text == "Blink":
                    pass 
            except Exception as e:
                print(f"Error in Blink Detection: {e}")

            try:
                # ---- Eye Gaze Detection ----
                eyeStatus = gazeDetection(faces, frame)
                record.append(eyeStatus)
                if eyeStatus in ["left", "right", "Left", "Right"]:
                     save_and_alert(frame, f"Head gaze: {eyeStatus}")
            except Exception as e:
                print(f"Error in Gaze Detection: {e}")

            try:
                # ---- Mouth Tracking ----
                mouthStatus = mouthTrack(faces, frame)
                record.append(mouthStatus)
                if mouthStatus == "Mouth Open":
                    save_and_alert(frame, "Mouth opened")
            except Exception as e:
                 print(f"Error in Mouth Tracking: {e}")

            try:
                # ---- Object Detection ----
                objectName = detectObject(frame)
                record.append(objectName)
                if len(objectName) > 1: 
                    save_and_alert(frame, f"Suspicious objects detected: {objectName}")
            except Exception as e:
                print(f"Error in Object Detection: {e}")

            try:
                # ---- Head Pose Detection ----
                headPose = head_pose_detection(faces, frame)
                record.append(headPose)
                if headPose in ["Head Left", "Head Right", "Head Up", "Head Down"]:
                    save_and_alert(frame, f"Head pose: {headPose}")
            except Exception as e:
                print(f"Error in Head Pose Detection: {e}")

        data_record.append(record)
        
        # Show frame
        cv2.imshow("Proctoring", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()

# ------------------ Stop Function ------------------
def stop_proctoring():
    global stop_flag
    stop_flag = True

# ------------------ Optional Threading Example ------------------
# t = threading.Thread(target=proctoringAlgo)
# t.start()
# ... call stop_proctoring() when needed
