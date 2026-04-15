import requests

BOT_TOKEN = "8527986741:AAHkfmkKD6-tsjDoZOTPRPYyrVsvemRhYb0"
CHAT_ID = "5511579171"

def send_telegram_alert(image_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': CHAT_ID, 'caption': caption}
    requests.post(url, files=files, data=data)
