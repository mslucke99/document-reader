#pip install SpeechRecognition
#pip install gtts

import speech_recognition as sr

## imports for speak()
from gtts import gTTS
import playsound 
import os

# imports for say()
import pyttsx3

#GLOBAL 
language = "en"
recog = sr.Recognizer()  #speech to text
engine = pyttsx3.init()  # text to speech
activate_word = "alexa"


# TEXT TO SPEECH
def speak(phrase):
    ''' Given a string, use google text to speeach and playsound packages to say the phrase
    Argument:
        phrase: a string with the phrase you want the computer to say out loud
    Returns: 
        None
    '''
    tts = gTTS(text=phrase, lang = language)
    file_name = "audio.mp3"
    if os.path.exists(file_name):
        os.remove(file_name)
    tts.save(file_name)
    playsound.playsound(file_name)

def say (phrase):
    engine.say(phrase)
    engine.runAndWait()


## SPEECH TO TEXT - LISTEN 
def listen_continuously(something_to_say = None):

    ## Say something
    if (something_to_say != None):
        say(something_to_say)
                    
    ## Listen
    with sr.Microphone() as source:

        #listens to the first 0.5 seconds of the microphone to minimize noise of audio
        # Note:  Python package (such as SciPy) that can apply filters to the files.
        #        which may be useful if we get a lot of errors in this process

        recog.adjust_for_ambient_noise(source, duration=0.5) 
        text = recog.listen(source)

    
        try:
            listen_txt = recog.recognize_google(text)
            listen_txt = listen_txt.lower()
            print(listen_txt)
            if (activate_word in listen_txt):
                return (listen_txt)
            else:                  
                return listen_continuously()

        except sr.UnknownValueError:
            return listen_continuously()
            

        except sr.RequestError:
            print("Could not open the api to perform speech to text transformation")
            return None
    
def get_command(something_to_say = None):
    ## Say something
    if (something_to_say != None):
        print("Which information do you want to listen to?")
        say(something_to_say)
        
    with sr.Microphone() as source:

        #listens to the first 0.5 seconds of the microphone to minimize noise of audio
        # Note:  Python package (such as SciPy) that can apply filters to the files.
        #        which may be useful if we get a lot of errors in this process

        recog.adjust_for_ambient_noise(source, duration=0.5) 

        text = recog.listen(source)

        try:
            ## listen
            listen_txt = recog.recognize_google(text)
            return (listen_txt)


        except sr.UnknownValueError:
            say("Sorry I could not understand you")
            return None

        except sr.RequestError:
            print("Could not open the api to perform speech to text transformation")
            return None


if __name__ == "__main__":
    say("Hello Laura")
    #speak("Hello Laura")
    while True:
        command = listen_continuously()
        print(command)
        if "exit" in command: 
            break

## delete everything before activate word 

