#
# This file is for various math related to rectangles that will help find the distance between rectangles
# 
# vertices are input as [[left, top],[left, bot],[right, top],[right, bot]]

def checkintersection(rect1, rect2):
    # do two rectangles intersect
    pass

def distance(rect1, rect2):
    # how far two rectangles nearest points are from each other
    pass

def dist_x(rect1, rect2):
    # how far to the left and right of each other two rectangles are
    pass

def dist_y(rect1, rect2):
    # difference between heights of the two rectangles in the image
    # TODO Add math to detect if 
    pass

def relatednessScore(rect1, rect2):
    # a score for how related the text boxes are likely to be.
    # This will not be valid in theory, but might work in practice.
    pass

def lineSlope(pt1, pt2):
    # returns the slope of the line between the two points
    return (pt1[1]-pt2[1])/(pt1[2]-pt2[2])

def tangentSlope(pt1, pt2):
    # returns the slope of a line tangent to two points
    return -1/lineSlope(pt1, pt2)

def checkLineIntersection(line1, line2):
    # checks if two lines intersect within their bounds
    intersectpt = getLineIntersection(line1, line2)
    if intersectpt[0] < min(line1[0][0], line1[1][0]) or intersectpt[0] < min(line2[0][0], line2[1][0]):
        return False
    elif intersectpt[0] > max(line1[0][0], line1[1][0]) or intersectpt[0] < max(line2[0][0], line2[1][0]):
        return False
    elif intersectpt[1] < min(line1[0][1], line1[1][1]) or intersectpt[1] < min(line2[0][1], line2[1][1]):
        return False
    elif intersectpt[1] > max(line1[0][1], line1[1][1]) or intersectpt[1] < max(line2[0][1], line2[1][1]):
        return False
    else:
        return True

def getLineIntersection(line1, line2):
    # gets the intersection of lines with
    slope1 = lineSlope(line1[0], line1[1])
    slope2 = lineSlope(line2[0], line2[1])
    interx = (slope1*line1[0][0]-slope2*line2[0][0])/(slope1-slope2)
    intery = line1[0][1]+slope1*(interx-line1[0][0]) #y2=y1+m(x2-x1)
    return (interx, intery)

