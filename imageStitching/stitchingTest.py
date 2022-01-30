import numpy as np
import cv2
'''
# Calcium
path1 = 'images/calcium{}.jpg' # GENERAL IMAGE PATH STRING FORMAT
images = [cv2.imread(path1.format(i)) for i in range(1,5)]
cropped = [img[200+(75*(i-1)):1500+(75*(i-1)), :] for i, img in enumerate(images)]
stitcher = cv2.Stitcher.create(mode=0)
(status, stitched) = stitcher.stitch(cropped)
'''

# FDA
path1 = 'images/FDA{}.jpg' # GENERAL IMAGE PATH STRING FORMAT
images = [cv2.imread(path1.format(i)) for i in range(1,7)]
cropped = [img[1300 + (90 * (i - 1)):2000 + (90 * (i - 1)), 600:1600] for i, img in enumerate(images)]
cropped = [cv2.cvtColor(cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_BINARY)[1], cv2.COLOR_GRAY2BGR) for img in cropped]
stitcher = cv2.Stitcher.create(mode=0)
(status, stitched) = stitcher.stitch(cropped)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
    # display the output stitched image to our screen
    # cv2.imwrite('fda_stitch.jpg', stitched)
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
# otherwise the stitching failed, likely due to not enough keypoints
# being detected
else:
    print("[INFO] image stitching failed ({})".format(status))

