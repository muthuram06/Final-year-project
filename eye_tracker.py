import dlib
import cv2
import numpy as np
import time
from violation_handler import handle_violation

# -------------------------------
# Load Face Landmark Model
# -------------------------------
shapePredictorModel = 'shape_predictor_model/shape_predictor_68_face_landmarks.dat'
shapePredictor = dlib.shape_predictor(shapePredictorModel)

# -------------------------------
# Gaze Violation Control
# -------------------------------
LAST_GAZE_TIME = 0
GAZE_COOLDOWN = 5   # seconds

# -------------------------------
# Utility Functions
# -------------------------------
def createMask(frame):
    height, width, _ = frame.shape
    return np.zeros((height, width), np.uint8)

def extractEye(mask, region, frame):
    cv2.polylines(mask, region, True, 255, 2)
    cv2.fillPoly(mask, region, 255)
    return cv2.bitwise_and(frame, frame, mask=mask)

def eyeSegmentationAndReturnWhite(img, side):
    h, w = img.shape
    if side == 'left':
        return cv2.countNonZero(img[:, :int(w/2)])
    else:
        return cv2.countNonZero(img[:, int(w/2):])

# -------------------------------
# MAIN EYE TRACKER
# -------------------------------
def gazeDetection(faces, frame):
    global LAST_GAZE_TIME

    font = cv2.FONT_HERSHEY_DUPLEX
    thickness = 2
    TrialRatio = 1.2

    leftEyeIdx = [36,37,38,39,40,41]
    rightEyeIdx = [42,43,44,45,46,47]

    gaze_result = "Looking Center"

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for face in faces:
        landmarks = shapePredictor(gray, face)

        leftEye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in leftEyeIdx], np.int32)
        rightEye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in rightEyeIdx], np.int32)

        mask = createMask(frame)
        eyes = extractEye(mask, [leftEye, rightEye], frame)

        lx1, lx2 = np.min(leftEye[:,0]), np.max(leftEye[:,0])
        ly1, ly2 = np.min(leftEye[:,1]), np.max(leftEye[:,1])
        rx1, rx2 = np.min(rightEye[:,0]), np.max(rightEye[:,0])
        ry1, ry2 = np.min(rightEye[:,1]), np.max(rightEye[:,1])

        leftEyeImg = eyes[ly1:ly2, lx1:lx2]
        rightEyeImg = eyes[ry1:ry2, rx1:rx2]

        leftGray = cv2.cvtColor(leftEyeImg, cv2.COLOR_BGR2GRAY)
        rightGray = cv2.cvtColor(rightEyeImg, cv2.COLOR_BGR2GRAY)

        leftTh = cv2.adaptiveThreshold(
            leftGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        rightTh = cv2.adaptiveThreshold(
            rightGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        leftWhite = eyeSegmentationAndReturnWhite(leftTh, 'left')
        rightWhite = eyeSegmentationAndReturnWhite(leftTh, 'right')

        if rightWhite > TrialRatio * leftWhite:
            gaze_result = "Looking Left"
        elif leftWhite > TrialRatio * rightWhite:
            gaze_result = "Looking Right"
        else:
            gaze_result = "Looking Center"

        # -------------------------------
        # 🚨 GAZE VIOLATION ALERT
        # -------------------------------
        now = time.time()
        if gaze_result in ["Looking Left", "Looking Right"]:
            if now - LAST_GAZE_TIME > GAZE_COOLDOWN:
                handle_violation(frame, gaze_result)
                LAST_GAZE_TIME = now

        cv2.putText(frame, gaze_result, (40, 110),
                    font, 1, (255, 0, 255), thickness)

    return gaze_result
