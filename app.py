import cv2
import numpy as np
import winsound
from datetime import datetime

from facial_detections import detectFace

data_record = []

frequency = 2500
duration = 500


def faceCount_detection(faceCount):
    if faceCount > 1:
        winsound.Beep(frequency, duration)
        return "Multiple faces detected"
    elif faceCount == 0:
        winsound.Beep(frequency, duration)
        return "No face detected"
    else:
        return "Face OK"


def proctoringAlgo():

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():
        print("Camera not accessible")
        return

    while True:

        ret, frame = cam.read()

        if not ret:
            continue

        record = []

        current_time = datetime.now().strftime("%H:%M:%S")
        record.append(current_time)

        faceCount, faces, frame = detectFace(frame)
        record.append(faceCount_detection(faceCount))

        data_record.append(record)

        cv2.imshow("Proctoring", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    proctoringAlgo()

    activityVal = "\n".join(map(str, data_record))

    with open("activity.txt", "w") as file:
        file.write(activityVal)
