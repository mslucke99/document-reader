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
    pass

def relatednessScore(rect1, rect2):
    # a score for how related the text boxes are likely to be.
    # This will not be valid in theory, but might work in practice.
    pass

def lineSlope(pt1, pt2):
    # returns the slope of the line between the two points
    return (pt1[1]-pt2[1])/(pt1[2]-pt2[2])

def tangentslope(pt1, pt2):
    # returns the slope of a line tangent to two points
    return -1/lineslope(pt1, pt2)