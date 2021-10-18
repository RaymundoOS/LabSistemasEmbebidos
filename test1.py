import speech_recognition as sr
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
r = sr.Recognizer()
mic = sr.Microphone(device_index= 2 ) 
with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

r.recognize_google(audio)