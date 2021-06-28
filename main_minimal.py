import cv2 as cv
import math
import pytesseract
#from gtts import gTTS
#import playsound 
#import os
import speechRecog
import textbound


cap = cv.VideoCapture(0)

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    alignment = textbound.checkmargins(frame)
    if alignment == 0:
        imgtxt = pytesseract.image_to_string(frame)

        print(imgtxt)
        if imgtxt != "" and imgtxt[0].isalnum():
            speechRecog.speak(imgtxt)
    elif alignment == 1:
        speechRecog.speak("The text is too low, could you move it up or the camera down?")
    elif alignment == 2:
        speechRecog.speak("It is too high, could you lower it?")
    elif alignment == 3:
        speechRecog.speak("Could you move the object to the left?")
    elif alignment == 4:
        speechRecog.speak("It is too far to the left. Could you move your camera to the left?")