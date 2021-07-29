
# Much of this code was made with inspiration from the following pages:
# https://github.com/spmallick/learnopencv/blob/master/TextDetectionEAST/textDetection.py
# https://learnopencv.com/deep-learning-based-text-detection-using-opencv-c-python/

import cv2 as cv
import math


# https://arxiv.org/abs/1704.03155v2
net = cv.dnn.readNet("frozen_east_text_detection.pb")
net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
print("using cpu for EAST")

confThreshold = 0.5

nmsThreshold = 0.4

inpWidth = 320

inpHeight = 320

margin_size = 0.065

outputLayers = []
outputLayers.append("feature_fusion/Conv_7/Sigmoid")
outputLayers.append("feature_fusion/concat_3")

############ Utility functions ############
def decode(scores, geometry, scoreThresh):
    detections = []
    confidences = []

    ############ CHECK DIMENSIONS AND SHAPES OF geometry AND scores ############
    assert len(scores.shape) == 4, "Incorrect dimensions of scores"
    assert len(geometry.shape) == 4, "Incorrect dimensions of geometry"
    assert scores.shape[0] == 1, "Invalid dimensions of scores"
    assert geometry.shape[0] == 1, "Invalid dimensions of geometry"
    assert scores.shape[1] == 1, "Invalid dimensions of scores"
    assert geometry.shape[1] == 5, "Invalid dimensions of geometry"
    assert scores.shape[2] == geometry.shape[2], "Invalid dimensions of scores and geometry"
    assert scores.shape[3] == geometry.shape[3], "Invalid dimensions of scores and geometry"
    height = scores.shape[2]
    width = scores.shape[3]
    for y in range(0, height):

        # Extract data from scores
        scoresData = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        anglesData = geometry[0][4][y]
        for x in range(0, width):
            score = scoresData[x]

            # If score is lower than threshold score, move to next x
            if(score < scoreThresh):
                continue

            # Calculate offset
            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]

            # Calculate cos and sin of angle
            cosA = math.cos(angle)
            sinA = math.sin(angle)
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # Calculate offset
            offset = ([offsetX + cosA * x1_data[x] + sinA * x2_data[x], offsetY - sinA * x1_data[x] + cosA * x2_data[x]])

            # Find points for rectangle
            p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
            p3 = (-cosA * w + offset[0],  sinA * w + offset[1])
            center = (0.5*(p1[0]+p3[0]), 0.5*(p1[1]+p3[1]))
            detections.append((center, (w,h), -1*angle * 180.0 / math.pi))
            confidences.append(float(score))

    # Return detections and confidences
    return [detections, confidences]

def get_bounds(frame):
    """
    gets the bounds of text in an image
    input: frame, an image
    output: the vertices of the text in an image
    """
    height_ = frame.shape[0]
    width_ = frame.shape[1]
    rW = width_ / float(inpWidth)
    rH = height_ / float(inpHeight)
    blob = cv.dnn.blobFromImage(frame, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

    net.setInput(blob)
    output = net.forward(outputLayers)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())

    # Get scores and geometry
    scores = output[0]
    geometry = output[1]
    [boxes, confidences] = decode(scores, geometry, confThreshold)

    # Apply NMS
    indices = cv.dnn.NMSBoxesRotated(boxes, confidences, confThreshold,nmsThreshold)
    bounds = []
    for i in indices:
        # get 4 corners of the rotated rect
        vertices = cv.boxPoints(boxes[i[0]])
        # scale the bounding box coordinates based on the respective ratios
        for j in range(4):
            vertices[j][0] = int(vertices[j][0]*rW)
            vertices[j][1] = int(vertices[j][1]*rH)
        bounds.append(vertices)
    return bounds
        #for j in range(4):
        #    p1 = (int(vertices[j][0]), int(vertices[j][1]))
        #    p2 = (int(vertices[(j + 1) % 4][0]), int(vertices[(j + 1) % 4][1]))

def checkmargins(frame, bounds=None):
    if not bounds:
        bounds = get_bounds(frame)

    height = frame.shape[0]
    width = frame.shape[1]
    conditions = []
    for vertex in bounds:
        for j in range(4):
            if vertex[j][0]/height < margin_size:
                conditions.append(1) # too high I think
            elif (height-vertex[j][0])/height < margin_size:
                conditions.append(2) # too low I think
            elif vertex[j][1]/width < margin_size:
                conditions.append(3) # too far to the left?
            elif (width-vertex[j][1])/width < margin_size:
                conditions.append(4) # too far to the right?
    return conditions
        #for j in range(4):
        #    p1 = (int(vertices[j][0]), int(vertices[j][1]))
        #    p2 = (int(vertices[(j + 1) % 4][0]), int(vertices[(j + 1) % 4][1]))