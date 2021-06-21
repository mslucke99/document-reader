import cv2 as cv
import math
import pytesseract

cap = cv.VideoCapture(0)

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    imgtxt = pytesseract.image_to_string(frame)

    print(imgtxt)
