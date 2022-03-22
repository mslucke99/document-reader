# Code to work with contours and performs polynomial approximation
import cv2
import numpy as np
from numpy.polynomial.polynomial import Polynomial


# Finds largest (most relevant) contour after preprocessing
def find_contours(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, thresh_img = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY)
    # Kernel shape is a cross due to rigid horizontal/vertical nature of borders
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 4))
    removed = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(removed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    cv2.drawContours(image=img, contours=c, contourIdx=-1, color=(0, 100, 0), thickness=3)
    return c


# Converts contour array into an array of tuples (x, y)
def reformat_contour(contour_in):
    contour_in = contour_in.ravel()
    points = []
    for i in range(0, len(contour_in), 2):
        x = contour_in[i]
        y = contour_in[i + 1]
        points.append((x, y))
    return points


def reparameterize(origin, target):
    return target[0] - origin[0], target[1] - origin[1]


# Lower left point: Sort for and Find lowest x-coord points
# Sort for and Find lowest y-coord from points found above
# Method assumes that left-right are lines and top-bottom are arbitrary curves
# Similar logic for other three points
def find_corners(contour):
    contour = contour.ravel()
    points = reformat_contour(contour)
    points.sort(key=lambda a: a[0])  # Sorts according to x-coord
    leftmost = []
    rightmost = []
    for point in points:
        if point[0] == points[0][0]:
            leftmost.append(point)
        elif point[0] == points[-1][0]:
            rightmost.append(point)
    leftmost.sort(key=lambda a: a[1])  # Sorts according to y-coord
    rightmost.sort(key=lambda a: a[1])  # Sorts according to y-coord
    return leftmost[-1], rightmost[-1], rightmost[0], leftmost[0]  # UL, UR, LR, LL


# Finds orthogonal distance of a point (x,y) from a given line
def orthogonal_distance(line, point):
    line = np.array(line)
    point = np.array(point)
    v_norm = np.sqrt(sum(line ** 2))
    proj_of_u_on_v = (np.dot(point, line) / v_norm ** 2) * line
    return float(np.sqrt(sum((point - proj_of_u_on_v) ** 2)))


def draw_neighborhoods(img, neighborhood_length):
    for i in range(0, img.shape[1], neighborhood_length):
        cv2.line(img, pt1=(i, 0), pt2=(i, img.shape[1]), color=(0, 0, 255))


# Assumes that left/right sides of contour coincide with edges of image
# Locates contour points that correspond with "top" and "bottom" sides of contour
def find_top_bottom_sides(img, contour, neighborhood_length=150, tolerance=10):
    # draw_neighborhoods(img, neighborhood_length)  # Visualizes neighborhoods, for debugging purposes
    # Find corners of bounding rectangle
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    lower_1, upper_left, upper_right, lower_2 = box[3], box[0], box[1], box[0]

    # Find line connecting upper two corners
    rect_line = [upper_right[0] - upper_left[0], upper_right[1] - upper_left[1]]  # Encodes slope of line
    cv2.line(img, pt1=upper_left, pt2=upper_right, color=(0, 200, 0), thickness=5)

    # Create neighborhoods
    img_width = img.shape[1]

    # Need to account for overflow, also subtract left/right sides
    num_neighborhoods = (img_width - 2) // neighborhood_length + 1
    neighborhoods = []
    for i in range(num_neighborhoods):
        neighborhoods.append([])

    # Sort contour points into neighborhoods
    points = reformat_contour(contour)
    for point in points:
        if point[0] != 0 and point[0] != img_width:
            neighborhoods[(point[0] - 1) // neighborhood_length].append(point)

    top_side_contours = []
    bottom_side_contours = []

    # For each neighborhood, find smallest/largest orthogonal distances
    # Smallest = top side, Largest = Bottom side
    for neighborhood in neighborhoods:
        distances = []
        if len(neighborhood) > 0:
            for point in neighborhood:
                new_point = reparameterize(upper_left, point)
                distances.append(orthogonal_distance(rect_line, new_point))
            max_distance, min_distance = max(distances), min(distances)
            for i, point in enumerate(neighborhood):
                if abs(distances[i] - min_distance) <= tolerance:
                    top_side_contours.append(point)
                elif abs(distances[i] - max_distance) <= tolerance:
                    bottom_side_contours.append(point)

    return top_side_contours, bottom_side_contours


# List returned is ordered from lowest to highest degree: [0, 1, 2]
def find_polynomial_fit(points):
    # Find best-fitting quadratic through least-squares regression
    poly_fit = Polynomial.fit([point[0] for point in points], [point[1] for point in points], 2)
    return poly_fit.convert().coef


# Only finds arc lengths of parabolic curves
def arc_length(parabola, x_higher, x_lower=0):
    points = []
    for x in range(x_lower, x_higher+1):  # May need to adjust interval for speed/accuracy
        points.append((x, parabola[0] + (x*parabola[1]) + (x*x*parabola[2])))
    deriv = [parabola[1], parabola[2]*2]
    return np.trapz(
        y=[np.sqrt(
            1 + (deriv[0] + (deriv[1]*p[0]))**2
        ) for p in points], x=[p[0] for p in points]
    )

