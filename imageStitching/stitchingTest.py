import numpy as np
import cv2
import timeit

start = timeit.timeit()


path1 = 'test/IMG_48{}.JPG' # GENERAL IMAGE PATH STRING FORMAT
images = [cv2.imread(path1.format(i)) for i in range(57,83,2)]
stitcher = cv2.Stitcher_create()

#likely to crash when nan or inf introduced
(status, stitched) = stitcher.stitch(images)


# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
# being detected
else:
 print("[INFO] image stitching failed ({})".format(status))

end = timeit.timeit()

print(end - start)
