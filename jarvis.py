# Core system modules
import os
import subprocess
import datetime

# Voice and audio handling
import pyttsx3
import speech_recognition as sr
import pyaudio

# Online utilities
import wikipedia
import pywhatkit
import webbrowser

# GUI automation
import pyautogui

# Fun extras
import pyjokes

# Environment variable handler
from decouple import config

# ✅ Global configuration (remove indentation here)
USER = config('USER')
HOSTNAME = config('BOT')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

sleep_mode = False

def open_in_chrome(url):
    subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', url])

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print('Listening.....')
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print(f"Say Something {USER} Sir!")
        return "None"

    return query

def greetMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour <= 12:
        talk(f"Good Morning {USER}, Sir!")
    elif hour > 12 and hour <= 18:
        talk(f"Good Afternoon {USER}, Sir!")
    else:
        talk(f"Good Evening {USER}, Sir!")
    talk(f"I am {HOSTNAME}. What is the task today?")

def run_jarvis():
    global sleep_mode
    query = take_command().lower()

    if 'hello' in query or 'hey' in query:
        talk("Hi sir! How can I help you?")

    elif 'tell me joke' in query:
        talk(pyjokes.get_joke())

    elif 'exit' in query:
        talk('Goodbye! Have a nice day boss')
        exit()

    elif 'play' in query:
        song = query.replace('play', "")
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        print(time)
        talk("Current time is " + time)

    elif 'open' in query:
        app = query.replace('open', "").strip()
        pyautogui.press('super')
        pyautogui.sleep(0.5)
        pyautogui.typewrite(app)
        pyautogui.sleep(1)
        pyautogui.press('enter')
        talk(f'Opening {app}')

    elif 'close' in query:
        talk('Closing sir!')
        pyautogui.hotkey('alt', 'f4')

    elif 'who is' in query:
        person = query.replace('who is', '')
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)

    elif 'remember that' in query:
        rememberMessage = query.replace('remember that', '')
        talk('Sir, you told me to remember that ' + rememberMessage)
        with open('remember.txt', "a") as remember:
            remember.write(rememberMessage + "\n")

    elif 'what do you remember' in query:
        with open('remember.txt', 'r') as remember:
            talk('Sir, you told me to remember: ' + remember.read())

    elif 'clear remember file' in query:
        with open('remember.txt', 'w') as file:
            file.write("")
        talk('Done Sir! Everything I remember has been deleted.')

    elif 'shutdown' in query:
        talk('Closing the PC in 3... 2... 1...')
        os.system("shutdown /s /t 1")

    elif 'restart' in query:
        talk('Restarting the PC in 3... 2... 1...')
        os.system("shutdown /r /t 1")

    elif 'search' in query:
        user_query = query.replace('search', '')
        print(f'User Query: {user_query}')
        url = f'https://www.google.com/search?q={user_query}'
        print(f'Search URL: {url}')
        open_in_chrome(url)
        talk('This is what I found on the internet.')

    elif 'stop' in query or 'start' in query:
        pyautogui.press('k')
        talk('Done sir!')

    elif 'theater screen' in query:
        pyautogui.press('t')
        talk('Done sir!')

    elif 'full screen' in query:
        pyautogui.press('f')
        talk('Done sir!')

    elif 'sleep' in query:
        talk('Okay sir! I am now in listening mode. Call me when you want me to wake up.')
        sleep_mode = True

        while sleep_mode:
            query = take_command().lower()
            if 'wake up' in query:
                talk(f'I am now in action mode, {USER} sir.')
                sleep_mode = False
                break

    else:
        talk("I don't understand!")

# ✅ Program entry point
greetMe()
while True:
    if not sleep_mode:
        run_jarvis()
