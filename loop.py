from datetime import datetime
import numpy as np
import sounddevice as sd
from cancellation import cancellation

duration = 1  # seconds
fs = 44100  # Sample rate

# Classify the loudness
def calculate_db(audio_data):
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)
    rms = np.sqrt(np.mean(audio_data**2))
    db = 20 * np.log10(rms)
    return db


def loop():
    while not cancellation.is_requested:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait()
        db = calculate_db(audio_data)
        print(datetime.now(), db)