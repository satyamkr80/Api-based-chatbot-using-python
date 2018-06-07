import speech_recognition as sr
from gtts import gTTS
import re

import json, requests 
from time import sleep

import pyttsx
engine=pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        print("Speak")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):

    if 'anaya' in command:
        reg_ex=re.search('anaya (.*)', command)
        if reg_ex:
            smalltalk=reg_ex.group(1)
            url = requests.get('http://192.168.43.202/AI/read_all.php?command='+smalltalk) 
            root= json.loads(url.text) 
            sleep(2) 
            result= root['response'] 
            print result
            engine.say(result)
            engine.runAndWait()
    


while True:
    assistant(myCommand())
