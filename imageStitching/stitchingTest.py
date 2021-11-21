import numpy as np
import cv2

path1 = 'clorox{}.jpg' # GENERAL IMAGE PATH STRING FORMAT
images = [cv2.imread(path1.format(i)) for i in range(1,10)]
stitcher = cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
        # display the output stitched image to our screen
        # cv2.imwrite("whiteboardstitch.jpg", stitched)
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
# otherwise the stitching failed, likely due to not enough keypoints
# being detected
else:
    print("[INFO] image stitching failed ({})".format(status))
