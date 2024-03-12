import pyttsx3
import datetime

from decouple import config

USER = config('USER')
HOSTNAME = config('BOT')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 250)

def talk(audio):
    engine.say(audio)
    engine.runAndWait()
    
