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
    if alignment == []: # if the text is aligned
        imgtxt = pytesseract.image_to_string(frame) # get the text from the image
        # text appears as multiple lines. The following will parse all the lines and say each one of them
        imgtxtlist = [line for line in imgtxt.split('\n') if line != "" and line[0].isalnum()]
        print(imgtxt)
        # if imgtxt != "" and imgtxt[0].isalnum():
        for line in imgtxtlist:
            speechRecog.speak(line) # will not say anything if there is no text, but this will still run
    elif alignment == [2]:
        speechRecog.speak("The text is too low, could you move it up or the camera down?")
        pt1 = ((frame_height*2)//3, (frame_length*1)//2)
        pt2 = ((frame_height*3)//4, (frame_length*1)//2)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
    elif alignment == [1]:
        speechRecog.speak("It is too high, could you lower it?")
        pt1 = ((frame_height*1)//3, (frame_length*1)//2)
        pt2 = ((frame_height*1)//4, (frame_length*1)//2)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
    elif alignment == [3]:
        speechRecog.speak("Could you move the object to the left?")
        pt1 = ((frame_height*1)//2, (frame_length*1)//3)
        pt2 = ((frame_height*1)//2, (frame_length*1)//4)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
    elif alignment == [4]:
        speechRecog.speak("It is too far to the left. Could you move your camera to the left?")
        pt1 = ((frame_height*1)//2, (frame_length*2)//3)
        pt2 = ((frame_height*1)//2, (frame_length*3)//4)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
    elif (1 in alignment and 2 in alignment) or (3 in alignment and 4 in alignment):
        speechRecog.speak("could you move the camera and object away from each other?")
        pt1 = ((frame_height*2)//3, (frame_length*1)//2)
        pt2 = ((frame_height*3)//4, (frame_length*1)//2)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
        pt1 = ((frame_height*1)//3, (frame_length*1)//2)
        pt2 = ((frame_height*1)//4, (frame_length*1)//2)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
        pt1 = ((frame_height*1)//2, (frame_length*1)//3)
        pt2 = ((frame_height*1)//2, (frame_length*1)//4)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
        pt1 = ((frame_height*1)//2, (frame_length*2)//3)
        pt2 = ((frame_height*1)//2, (frame_length*3)//4)
        cv.arrowedLine(frame, pt1, pt2, (255, 165, 0), thickness=5)
    elif (1 in alignment and 3 in alignment):
        pass
    elif (1 in alignment and 4 in alignment):
        pass
    elif (2 in alignment and 3 in alignment):
        pass
    elif (2 in alignment and 4 in alignment):
        pass
    
    # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    # Display the frame
    cv.imshow(kWinName,frame)
    cv.imwrite("output.png",frame)