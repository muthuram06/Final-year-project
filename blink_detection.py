import dlib
import cv2
import time
from math import hypot
from violation_handler import handle_violation

# -------------------------------
# Load Landmark Model
# -------------------------------
shapePredictorModel = 'shape_predictor_model/shape_predictor_68_face_landmarks.dat'
shapePredictor = dlib.shape_predictor(shapePredictorModel)

# -------------------------------
# Blink Control
# -------------------------------
BLINK_COUNT = 0
LAST_BLINK_ALERT = 0
BLINK_COOLDOWN = 6          # seconds
BLINK_LIMIT = 25            # excessive blink threshold

# -------------------------------
# Utility Functions
# -------------------------------
def midPoint(pointA, pointB):
    X = int(pointA.x + pointB.x) / 2
    Y = int(pointA.y + pointB.y) / 2
    return (X, Y)

def findDist(pointA, pointB):
    return hypot(pointA[0] - pointB[0], pointA[1] - pointB[1])

# -------------------------------
# MAIN BLINK DETECTOR
# -------------------------------
def isBlinking(faces, frame):
    global BLINK_COUNT, LAST_BLINK_ALERT

    font = cv2.FONT_HERSHEY_PLAIN
    thickness = 2

    blink_status = "No Blink"
    lRatio = rRatio = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    for face in faces:
        landmarks = shapePredictor(gray, face)

        # LEFT EYE
        lLeft = (landmarks.part(36).x, landmarks.part(36).y)
        lRight = (landmarks.part(39).x, landmarks.part(39).y)
        lTop = midPoint(landmarks.part(37), landmarks.part(38))
        lBottom = midPoint(landmarks.part(40), landmarks.part(41))

        leftHor = findDist(lLeft, lRight)
        leftVer = findDist(lTop, lBottom)

        # RIGHT EYE
        rLeft = (landmarks.part(42).x, landmarks.part(42).y)
        rRight = (landmarks.part(45).x, landmarks.part(45).y)
        rTop = midPoint(landmarks.part(43), landmarks.part(44))
        rBottom = midPoint(landmarks.part(46), landmarks.part(47))

        rightHor = findDist(rLeft, rRight)
        rightVer = findDist(rTop, rBottom)

        lRatio = leftHor / leftVer
        rRatio = rightHor / rightVer

        # -------------------------------
        # BLINK DETECTION
        # -------------------------------
        if lRatio >= 3.6 or rRatio >= 3.6:
            BLINK_COUNT += 1
            blink_status = "Blink"
            cv2.putText(frame, "Blink", (50,140),
                        font, 2, (0, 0, 255), thickness)
        else:
            blink_status = "No Blink"

        # -------------------------------
        # 🚨 EXCESSIVE BLINK ALERT
        # -------------------------------
        current_time = time.time()
        if BLINK_COUNT >= BLINK_LIMIT:
            if current_time - LAST_BLINK_ALERT > BLINK_COOLDOWN:
                handle_violation(frame, "Excessive_Blinking")
                LAST_BLINK_ALERT = current_time
                BLINK_COUNT = 0   # reset after alert

    return (lRatio, rRatio, blink_status)
