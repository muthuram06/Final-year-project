import time


class BehaviorAnalytics:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.reset_window()

    # ===============================
    # Reset Window
    # ===============================
    def reset_window(self):
        self.start_time = time.time()

        self.blink_count = 0
        self.head_changes = 0
        self.prev_head = None

        self.total_frames = 0
        self.face_missing_frames = 0
        self.multi_face_count = 0
        self.device_frames = 0
        self.external_voice_frames = 0

    # ===============================
    # Update Per Frame
    # ===============================
    def update(self,
               head_value,
               blink_flag,
               multi_face_flag,
               device_flag,
               external_voice_flag):

        self.total_frames += 1

        # Device detection
        if device_flag == 1:
            self.device_frames += 1

        # External voice detection
        if external_voice_flag == 1:
            self.external_voice_frames += 1

        # Blink
        if blink_flag == 1:
            self.blink_count += 1

        # Head movement change
        if self.prev_head is not None:
            if head_value != self.prev_head and head_value != 99:
                self.head_changes += 1

        self.prev_head = head_value

        # Face absence
        if head_value == 99:
            self.face_missing_frames += 1

        # Multi-face detection
        if multi_face_flag == 1:
            self.multi_face_count += 1

        # Check window completion
        if time.time() - self.start_time >= self.window_size:
            return self.compute_metrics()

        return None

    # ===============================
    # Compute Metrics
    # ===============================
    def compute_metrics(self):

        if self.total_frames == 0:
            self.reset_window()
            return None

        # Use total_frames for stable normalization
        blink_rate = self.blink_count / self.total_frames
        head_movement_rate = self.head_changes / self.total_frames
        face_absence_ratio = self.face_missing_frames / self.total_frames
        multi_face_rate = self.multi_face_count / self.total_frames
        device_rate = self.device_frames / self.total_frames
        voice_rate = self.external_voice_frames / self.total_frames

        metrics = {
            "blink_rate": round(blink_rate, 3),
            "head_movement_rate": round(head_movement_rate, 3),
            "face_absence_ratio": round(face_absence_ratio, 3),
            "multi_face_rate": round(multi_face_rate, 3),
            "device_rate": round(device_rate, 3),
            "voice_rate": round(voice_rate, 3)
        }

        self.reset_window()
        return metrics