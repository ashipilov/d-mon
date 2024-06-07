import sounddevice as sd
import numpy as np
from scipy.signal import butter, lfilter
from cancellation import cancellation


duration = 5
sample_rate = 44100

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def calculate_rms(data):
    return np.sqrt(np.mean(data**2))

def detect_loudness(duration=5, sample_rate=44100, lowcut=85.0, highcut=3000.0):
    print("Recording...")
    # Record audio for the specified duration (5 seconds)
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    
    # Apply bandpass filter to the recording
    filtered_recording = bandpass_filter(recording[:, 0], lowcut, highcut, sample_rate)
    
    # Calculate the RMS value of the filtered recording
    rms_value = calculate_rms(filtered_recording)
    print(f"RMS loudness value: {rms_value}")
    return rms_value


def loop():
    while not cancellation.is_requested:
        peak_noise = detect_loudness()
        print(f"Detected peak noise level: {peak_noise}")