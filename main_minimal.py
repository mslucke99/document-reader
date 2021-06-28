import cv2 as cv
import math
import pytesseract
#from gtts import gTTS
#import playsound 
#import os
import speechRecog


cap = cv.VideoCapture(0)

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    imgtxt = pytesseract.image_to_string(frame)

    print(imgtxt)
    if imgtxt != "" and imgtxt[0].isalnum():
        speechRecog.speak(imgtxt)
