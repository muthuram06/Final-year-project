import cv2
from datetime import datetime
from telegram_alert import send_telegram_alert

def handle_violation(frame, reason):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"violations/{reason}_{timestamp}.jpg"

    cv2.imwrite(image_path, frame)

    caption = f"""
🚨 PROCTORING VIOLATION 🚨
Reason : {reason}
Time   : {timestamp}
"""

    send_telegram_alert(image_path, caption)
