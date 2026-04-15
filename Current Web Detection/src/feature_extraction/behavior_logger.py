import csv
import time


class BehaviorLogger:
    def __init__(self, filename="behavior_log.csv"):
        self.filename = filename
        self.start_time = time.time()

        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "head_direction",
                "blink_flag",
                "predicted_label"
            ])

    def log(self, head_value, blink_value,predicted_label):
        current_time = time.time() - self.start_time

        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                round(current_time, 3),
                head_value,
                blink_value,
                predicted_label
            ])