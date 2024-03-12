import pyttsx3
import speech_recognition 
import datetime
import pyaudio
import pyjokes
import pywhatkit
import pyautogui
import wikipedia
import os
import webbrowser
import subprocess  

from decouple import config

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
        audio= r.listen(source,0,4)

    try:
        print("Understanding.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")

    except Exception as e:                         
        print("Say Something {USER} Sir!")
        return "None" 
    
    return query

def greetMe(): 
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<=12:
        talk(f"Good Morning {USER}, Sir!")
    elif hour >12 and hour<=18:
        talk(f"Good Afternoon {USER}, Sir!")
    else: 
        talk(f"Good Evening {USER}, Sir!")
    talk(f"I am {HOSTNAME}. what is task today") 

def run_jarvis():
    global sleep_mode
    query = take_command()

    if 'hello' in query or 'hey' in query:
        talk("hi sir! how can i help you")
    
    elif 'tell me joke' in query:
        talk(pyjokes.get_joke())

    elif 'exit' in query :
        talk('goodBye! have a nice day boss')
        exit()

    elif 'play' in query:
        song = query.replace('play', "")
        talk('playing' + song)
        pywhatkit.playonyt(song)

    elif 'time' in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        print(time)
        talk("Current time is"+ time)
    
    elif 'open' in query:
        query = query.replace('open', "")
        pyautogui.press('super')
        pyautogui.sleep(0.5)
        pyautogui.typewrite(query)
        pyautogui.sleep(1)
        pyautogui.press('enter')
        talk('opening {query}')

    elif 'close' in query:
        talk('closing sir!')
        pyautogui.hotkey('alt', 'f4')

    elif 'who is' in query:
        person = query.replace('who is', '')
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)

    elif 'remember that' in query:
        rememberMessage = query.replace('remember that', '')
        talk('sir you told me to remember that' + rememberMessage)
        remember = open('remember.txt', "a")
        remember.write(rememberMessage)
        remember.close

    elif 'what do you remember' in query:
        remember = open('remember.txt', 'r')
        talk('sir yo told me to remember' + remember.read())

    elif 'clear remember file' in query:
        file = open('remember.txt', 'w')
        file.write(f"")
        talk('Done Sir! everything i remember has been deleted.')

    elif 'shutdown' in query:
        talk('closing the pc in')
        talk('3. 2. 1')
        os.system("shutdown /s /t 1")

    elif 'restart' in query:
        talk('restarting the pc in')
        talk('3. 2. 1')
        os.system("shutdown /r /t 1")

    elif 'search' in query:
        user_query = query.replace('search', '')
        print(f'User Query: {user_query}')  # Print user query for debugging
        url = f'https://www.google.com/search?q={user_query}'
        print(f'Search URL: {url}')  # Print search URL for debugging
        open_in_chrome(url)
        talk('This is what I found on the internet.')

    elif 'stop' in query or 'start' in query:
        pyautogui.press('k')
        talk('done sir!')

    elif 'theater screen' in query:
        pyautogui.press('t')
        talk('done sir!')

    elif 'full screen' in query:
        pyautogui.press('f')
        talk('done sir!')

    elif 'sleep' in query:
        talk('Okay sir! I am now in listening mode. Call me when you want me to wake up.')
        sleep_mode = True

        # Keep listening until wake-up command
        while sleep_mode:
            query = take_command()

            if 'wake up' in query:
                talk(f'I am now in Action mode {USER} sir')
                sleep_mode = False
                break

    else :
        talk("I Don't Understand!")


greetMe()  
while True:
     if not sleep_mode:
        run_jarvis()
    


   




