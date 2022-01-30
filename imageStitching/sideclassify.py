import cv2
i = 4
filepath = f"images/fda{i}.jpg"
img = cv2.imread(filepath)
img = img[1500 + (90 * (i - 1)):2000 + (90 * (i - 1)), 600:1500]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.cvtColor(cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_BINARY)[1],
                           cv2.COLOR_GRAY2BGR)

# apply canny edge detection
edges = cv2.Canny(img, 90, 130)

# apply morphology close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# get contours and keep largest
contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours = contours[0] if len(contours) == 2 else contours[1]
big_contour = max(contours, key=cv2.contourArea)

# draw contour
contour = img.copy()
cv2.drawContours(contour, [big_contour], 0, (0,0,255), 1)

# get number of vertices (sides)
peri = cv2.arcLength(big_contour, True)
approx = cv2.approxPolyDP(big_contour, 0.03 * peri, True)
print('number of sides:',len(approx))

# show result
cv2.imshow("edges", edges)
cv2.imshow("morph", morph)
cv2.imshow("contour", contour)
cv2.waitKey(0)
cv2.destroyAllWindows()