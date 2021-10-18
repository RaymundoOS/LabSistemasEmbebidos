import speech_recognition as sr
import pyaudio
r = sr.Recognizer()
hola = sr.AudioFile('Hola.wav')
with hola as source:
    audio = r.record(source)
r.recognize_google(audio)