import cv2
import numpy as np
import mediapipe as mp

from feature_extraction.behavior_logger import BehaviorLogger
from behavior_analytics import BehaviorAnalytics
from models.risk_model import RiskModel
from adaptive_learning.baseline_builder import BaselineBuilder
from adaptive_learning.continual_update import ContinualUpdater
from models.temporal_smoother import TemporalRiskSmoother
from feature_extraction.device_detector import DeviceDetector
from feature_extraction.audio_detector import AudioDetector


# ===============================
# MediaPipe Setup
# ===============================

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


# ===============================
# Feature Functions
# ===============================

def eye_aspect_ratio(landmarks, eye_indices):
    p1 = np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y])
    p2 = np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y])
    p3 = np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])
    p4 = np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y])
    p5 = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    p6 = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])

    vertical = np.linalg.norm(p1 - p2) + np.linalg.norm(p3 - p4)
    horizontal = np.linalg.norm(p5 - p6)

    if horizontal == 0:
        return 0

    return vertical / (2.0 * horizontal)


def get_head_direction(landmarks):
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    nose = landmarks[1]

    eye_center_x = (left_eye.x + right_eye.x) / 2
    diff = nose.x - eye_center_x

    if diff > 0.02:
        return "Right", 1
    elif diff < -0.02:
        return "Left", -1
    else:
        return "Center", 0


# ===============================
# Main Pipeline
# ===============================

def run_head_pose():

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not working")
        return

    device_detector = DeviceDetector()
    audio_detector = AudioDetector()

    logger = BehaviorLogger("behaviour_log.csv")
    analytics = BehaviorAnalytics(window_size=5)
    risk_model = RiskModel()
    baseline_builder = BaselineBuilder(required_windows=6)
    continual_updater = ContinualUpdater(alpha=0.05)
    risk_smoother = TemporalRiskSmoother(alpha=0.3)

    baseline_profile = None
    current_risk_level = "CALIBRATING"
    last_metrics = {}

    BLINK_THRESHOLD = 0.3
    blink_display_count = 0
    blink_cooldown = False
    COOLDOWN_FRAMES = 5
    cooldown_counter = 0

    frame_counter = 0
    YOLO_INTERVAL = 5
    device_flag = 0
    external_voice_flag = 0
    last_rms = 0.0

    print("Recording behavior... Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (800, 600))
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb_frame)

        head_value = 0
        blink_flag = 0
        multi_face_flag = 0
        direction = "N/A"
        avg_ear = 0

        # ===============================
        # FACE PROCESSING
        # ===============================

        if results.multi_face_landmarks:

            if len(results.multi_face_landmarks) > 1:
                multi_face_flag = 1

            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark

                direction, head_value = get_head_direction(landmarks)

                left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
                right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
                avg_ear = (left_ear + right_ear) / 2.0

                if avg_ear < BLINK_THRESHOLD and not blink_cooldown:
                    blink_flag = 1
                    blink_display_count += 1
                    blink_cooldown = True
                    cooldown_counter = 0

                if blink_cooldown:
                    cooldown_counter += 1
                    if cooldown_counter > COOLDOWN_FRAMES:
                        blink_cooldown = False

                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION
                )

        else:
            head_value = 99
            direction = "Face Missing"

        # ===============================
        # DEVICE DETECTION (Optimized)
        # ===============================

        frame_counter += 1
        if frame_counter % YOLO_INTERVAL == 0:
            devices = device_detector.detect(frame)
            device_flag = 1 if len(devices) > 0 else 0

        # ===============================
        # ANALYTICS
        # ===============================

        logger.log(head_value, blink_flag, predicted_label=0)

        metrics = analytics.update(
            head_value,
            blink_flag,
            multi_face_flag,
            device_flag,
            external_voice_flag
        )

        if metrics is not None:

            external_voice_flag, last_rms = audio_detector.detect_external_voice()

            last_metrics = metrics

            if baseline_profile is None:
                baseline_builder.update(metrics)
                if baseline_builder.is_ready():
                    baseline_profile = baseline_builder.compute_baseline()
                    current_risk_level = "MONITORING"

            else:
                risk_output = risk_model.classify(metrics, baseline_profile)
                smoothed_score = risk_smoother.smooth(
                    risk_output["risk_score"]
                )

                baseline_profile = continual_updater.update_baseline(
                    baseline_profile,
                    metrics
                )

                if smoothed_score >= risk_model.high_threshold:
                    current_risk_level = "HIGH RISK"
                elif smoothed_score >= risk_model.medium_threshold:
                    current_risk_level = "MEDIUM RISK"
                else:
                    current_risk_level = "LOW RISK"

        # ===============================
        # DISPLAY ALL DETAILS
        # ===============================

        y = 30

        cv2.putText(frame, f"Head Position: {direction}", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y += 30

        cv2.putText(frame, f"EAR: {round(avg_ear,3)}", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        y += 30

        cv2.putText(frame, f"Blink Count: {blink_display_count}", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        y += 30

        if last_metrics:
            cv2.putText(frame,
                        f"Blink Rate: {last_metrics.get('blink_rate',0)}",
                        (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 0, 255),
                        2)
            y += 30

        cv2.putText(frame,
                    f"Sound RMS: {round(last_rms,4)}",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2)
        y += 30

        if external_voice_flag:
            cv2.putText(frame,
                        "External Voice: DETECTED",
                        (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2)
        else:
            cv2.putText(frame,
                        "External Voice: Normal",
                        (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2)
        y += 30

        cv2.putText(frame, f"Risk Level: {current_risk_level}",
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255) if current_risk_level == "HIGH RISK" else
                    (0, 165, 255) if current_risk_level == "MEDIUM RISK" else
                    (0, 255, 0),
                    2)

        cv2.imshow("Smart Proctoring System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if risk_output["risk_level"] == "HIGH RISK":
        predicted_label = 1
    else:
        predicted_label = 0
    
    cap.release()
    cv2.destroyAllWindows()
    print("Behavior log saved successfully.")