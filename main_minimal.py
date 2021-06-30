import cv2 as cv
import math
import pytesseract
#from gtts import gTTS
#import playsound 
#import os
import speechRecog
import textbound


cap = cv.VideoCapture(0)

kWinName = "visualization"
cv.namedWindow(kWinName, cv.WINDOW_NORMAL)


while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    frame_height = frame.shape[0]
    frame_length = frame.shape[1]
    alignment = textbound.checkmargins(frame)
    if alignment == 0:
        imgtxt = pytesseract.image_to_string(frame)

        print(imgtxt)
        if imgtxt != "" and imgtxt[0].isalnum():
            speechRecog.speak(imgtxt)
    elif alignment == 1:
        speechRecog.speak("The text is too low, could you move it up or the camera down?")
        pt1 = ((frame_height*2)//3, (frame_length*1)//2)
        pt2 = ((frame_height*3)//4, (frame_length*1)//2)
        cv.arrowedline(frame, pt1, pt2, "Orange")
    elif alignment == 2:
        speechRecog.speak("It is too high, could you lower it?")
        pt1 = ((frame_height*1)//3, (frame_length*1)//2)
        pt2 = ((frame_height*1)//4, (frame_length*1)//2)
        cv.arrowedline(frame, pt1, pt2, "Orange")
    elif alignment == 3:
        speechRecog.speak("Could you move the object to the left?")
        pt1 = ((frame_height*1)//2, (frame_length*1)//3)
        pt2 = ((frame_height*1)//2, (frame_length*1)//4)
        cv.arrowedline(frame, pt1, pt2, "Orange")
    elif alignment == 4:
        speechRecog.speak("It is too far to the left. Could you move your camera to the left?")
        pt1 = ((frame_height*1)//2, (frame_length*2)//3)
        pt2 = ((frame_height*1)//2, (frame_length*3)//4)
        cv.arrowedline(frame, pt1, pt2, "Orange")

    # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    # Display the frame
    cv.imshow(kWinName,frame)
    cv.imwrite("output.png",frame)