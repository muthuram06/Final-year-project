import cv2
import numpy as np

# Load OpenCV Haar Cascade (built-in)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detectFace(frame):

    if frame is None:
        return 0, [], frame

    # Ensure uint8
    frame = np.asarray(frame, dtype=np.uint8)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    faceCount = len(faces)

    # Draw rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return faceCount, faces, frame
