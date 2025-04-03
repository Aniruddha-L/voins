import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

duration = 5
samplerate = 96000 
def record():
    print("Recording...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    wav_filename = "recorded_audio.wav"
    wav.write(wav_filename, samplerate, audio_data) 
    return 1