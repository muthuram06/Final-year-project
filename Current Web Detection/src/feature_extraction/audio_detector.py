import numpy as np
import sounddevice as sd


class AudioDetector:

    def __init__(self, duration=0.8, threshold=0.0015):
        self.duration = duration
        self.threshold = threshold
        self.device_index = 9  # Your WASAPI mic

        device_info = sd.query_devices(self.device_index)
        self.sample_rate = int(device_info["default_samplerate"])

        print("Using sample rate:", self.sample_rate)

    def detect_external_voice(self):
        try:
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                device=self.device_index
            )
            sd.wait()

            # RMS calculation
            rms = np.sqrt(np.mean(recording ** 2))

            detected = 1 if rms > self.threshold else 0

            return detected, rms

        except Exception as e:
            print("Audio Error:", e)
            return 0, 0.0