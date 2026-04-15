import cv2
import numpy as np
import pyaudio
import winsound
import time

# -------------------------------
# Beep Settings (Windows)
# -------------------------------
FREQUENCY = 2500   # Hz
DURATION = 1000    # ms

# -------------------------------
# Audio Detection Function
# -------------------------------
def audio_detection():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    THRESHOLD = 2000      # Adjust based on environment
    COOLDOWN_TIME = 3     # Seconds between detections

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🎧 Audio monitoring started... Press Ctrl+C to stop")

    last_detected_time = 0

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            amplitude = np.max(np.abs(audio_data))
            current_time = time.time()

            # Check for suspicious sound
            if amplitude > THRESHOLD and (current_time - last_detected_time) > COOLDOWN_TIME:
                print(f"⚠ Suspicious audio detected! Amplitude: {amplitude}")

                # Beep alert
                winsound.Beep(FREQUENCY, DURATION)

                # Capture camera frame
                capture_and_save_frame()

                last_detected_time = current_time

    except KeyboardInterrupt:
        print("\n🛑 Audio detection stopped")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# -------------------------------
# Camera Capture Function
# -------------------------------
def capture_and_save_frame():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    ret, frame = cap.read()

    if ret:
        filename = f"suspicious_frame_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Frame captured: {filename}")

    cap.release()

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    audio_detection()
