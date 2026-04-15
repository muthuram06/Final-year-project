import dlib
import cv2
from math import hypot

# -------------------------------
# Load Shape Predictor ONCE
# -------------------------------
PREDICTOR_PATH = "shape_predictor_model/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(PREDICTOR_PATH)

# -------------------------------
# Distance Calculation
# -------------------------------
def calcDistance(pointA, pointB):
    return hypot(pointA[0] - pointB[0], pointA[1] - pointB[1])

# -------------------------------
# Mouth Tracking Function
# -------------------------------
def mouthTrack(faces, frame):
    """
    Input : detected faces, BGR frame
    Output: status ("Mouth Open" / "Mouth Closed"), mouth distance
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mouth_status = "No Face"
    mouth_distance = 0

    for face in faces:
        landmarks = predictor(gray, face)

        # Outer lip landmarks
        top_lip = (landmarks.part(51).x, landmarks.part(51).y)
        bottom_lip = (landmarks.part(57).x, landmarks.part(57).y)

        # Distance between lips
        mouth_distance = calcDistance(top_lip, bottom_lip)

        # Threshold (tune if needed)
        MOUTH_OPEN_THRESHOLD = 23

        if mouth_distance > MOUTH_OPEN_THRESHOLD:
            mouth_status = "Mouth Open"
            color = (0, 0, 255)
        else:
            mouth_status = "Mouth Closed"
            color = (0, 255, 0)

        # Display result
        cv2.putText(frame, mouth_status, (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        cv2.putText(frame, f"Distance: {int(mouth_distance)}", (50, 115),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Track only first face
        break

    return mouth_status, mouth_distance
