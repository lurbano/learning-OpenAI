import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from transformers import pipeline

transcriber = pipeline(task="automatic-speech-recognition", model="openai/whisper-base")

# Set the sample rate and duration for recording
sd.default.samplerate = fs = 44100
duration = 15  # Recording duration in seconds (5 minutes)

dt = 5.0  # length of each clip in seconds
ct = 0

audioDir = "audio/"
audioData = np.array([])

transcript = ''


def fname(x, kind="rec"):
    if kind == "rec":
        prefix = "rec"
        ftype = "wav"
    else:
        prefix = kind
        ftype = "txt"
    return f"{audioDir}{prefix}{str(x).zfill(4)}.{ftype}"

def callback(indata, frames, t, status):
    global ct
    global startTime
    global audioData
    global transcript
    if status:
        print(status, flush=True)


    audioData = np.append(audioData, indata)
    if ((time.monotonic() - startTime) >= dt):
        startTime = time.monotonic()
        # Save the audio data to a WAV file with a unique filename based on timestamp
        filename = fname(ct)
        ct += 1
        sf.write(filename, audioData, fs)
        x = transcriber(filename)
        print(x)
        with open(fname(ct, "trans"), "w") as f:
            f.write(x['text'])
        transcript += x['text']
        #wavio.write(filename, indata[0], sample_rate, sampwidth=3)
        print(f"Audio saved to {filename}")
        audioData = np.array([])
        
print("Start...")
startTime = time.monotonic()
# Start recording using sounddevice
with sd.InputStream(callback=callback, channels=1):
    sd.sleep(int(duration * 1000))

print("Done")
print(transcript)