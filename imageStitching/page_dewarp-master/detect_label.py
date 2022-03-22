import cv2
import sys


# Used when sorting contours by size
def sort_contour_key(ind_contour):
    return cv2.contourArea(ind_contour)


# Determines if a contour is rectangular
def determine_rectangular(ind_contour):
    length = cv2.arcLength(ind_contour, True)
    approx = cv2.approxPolyDP(ind_contour, 0.1 * length, True)
    return len(approx) == 4


# Used when determining corners of bounding rectangle
def x_key(coordinate):
    return coordinate[0]


# Used when determining corners of bounding rectangle
def y_key(coordinate):
    return coordinate[1]


# Returns a cropped image that focuses on any rectangular contours in the image
# Used for automatic cropping in page de-warping algorithm
def auto_crop(img):
    contour_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    th, contour_img = cv2.threshold(contour_img, 80, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(contour_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest area contours
    contours = list(contours)
    contours.sort(reverse=True, key=sort_contour_key)

    # Takes 0.05% largest contours
    contours = contours[:int(0.0005 * len(contours))]

    rectangular_contours = []
    for contour in contours:
        if determine_rectangular(contour):
            rectangular_contours.append(contour)

    cropped_imgs = []
    for contour in rectangular_contours:
        x, y, w, h = cv2.boundingRect(contour)
        box = [(x, y), (x, y + h), (x + w, y), (x + w, y + h)]

        # Order: Top Left [0], Top Right [1], Bottom Left [2], Bottom Right [3]
        box.sort(key=x_key)
        box.sort(key=y_key)

        # Determine boundaries of cropping, give some leeway (5%) based on dimensions of rectangle
        lower_bound = int(box[0][1] - 0.08 * (box[2][1] - box[0][1]))
        lower_bound = lower_bound if lower_bound >= 0 else 0

        upper_bound = int(box[2][1] + 0.08 * (box[2][1] - box[0][1]))
        upper_bound = upper_bound if upper_bound < img.shape[0] else img.shape[0]

        left_bound = int(box[2][0] - 0.08 * (box[3][0] - box[2][0]))
        left_bound = left_bound if left_bound >= 0 else 0

        right_bound = int(box[3][0] + 0.08 * (box[3][0] - box[2][0]))
        right_bound = right_bound if right_bound < img.shape[1] else img.shape[1]

        new_img = img[lower_bound:upper_bound, left_bound:right_bound]
        cropped_imgs.append(new_img)

    return cropped_imgs



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No image input!")
    else:

        # Read in and find all contours
        img = cv2.imread(sys.argv[1])
        if img is None:
            print("That image was not found.")
        else:
            contour_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            th, contour_img = cv2.threshold(contour_img, 80, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(contour_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Find the largest area contours
            contours = list(contours)
            contours.sort(reverse=True, key=sort_contour_key)

            # Takes 0.05% largest contours
            contours = contours[:int(0.0005 * len(contours))]

            rectangular_contours = []
            for contour in contours:
                if determine_rectangular(contour):
                    rectangular_contours.append(contour)

            '''
            cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=5)
            cv2.imshow("contours", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            cv2.drawContours(image=img, contours=rectangular_contours, contourIdx=-1, color=(255, 0, 0), thickness=8)
            cv2.imshow("contours simplified", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''

            cropped_imgs = []
            for contour in rectangular_contours:
                x, y, w, h = cv2.boundingRect(contour)
                box = [(x, y), (x, y+h), (x+w, y), (x+w, y+h)]

                # Order: Top Left [0], Top Right [1], Bottom Left [2], Bottom Right [3]
                box.sort(key=x_key)
                box.sort(key=y_key)

                '''
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("box", img)
                '''

                # Determine boundaries of cropping, give some leeway (5%) based on dimensions of rectangle
                lower_bound = int(box[0][1] - 0.08 * (box[2][1] - box[0][1]))
                lower_bound = lower_bound if lower_bound >= 0 else 0

                upper_bound = int(box[2][1] + 0.08 * (box[2][1] - box[0][1]))
                upper_bound = upper_bound if upper_bound < img.shape[0] else img.shape[0]

                left_bound = int(box[2][0] - 0.08 * (box[3][0] - box[2][0]))
                left_bound = left_bound if left_bound >= 0 else 0

                right_bound = int(box[3][0] + 0.08 * (box[3][0] - box[2][0]))
                right_bound = right_bound if right_bound < img.shape[1] else img.shape[1]

                new_img = img[lower_bound:upper_bound, left_bound:right_bound]
                cv2.imshow("crop", new_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
