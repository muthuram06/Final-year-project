from ultralytics import YOLO
import cv2


class DeviceDetector:

    def __init__(self):
        self.model = YOLO("yolov8s.pt")

        # Only target cheating-related devices
        self.target_classes = ["cell phone", "laptop", "tablet"]

        self.conf_threshold = 0.20

        print("YOLO model loaded successfully")

    def detect(self, frame):

        detected_devices = []

        results = self.model(frame, verbose=False)

        for r in results:
            for box in r.boxes:

                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.model.names[cls_id]

                if (
                    class_name in self.target_classes
                    and conf > self.conf_threshold
                ):

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # 🔴 RED BOX FOR DEVICE
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),  # RED
                        3
                    )

                    # 🔴 CLEAR LABEL
                    cv2.putText(
                        frame,
                        f"DEVICE DETECTED ({class_name})",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

                    detected_devices.append(class_name)

        return detected_devices