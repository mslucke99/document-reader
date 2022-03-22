import cv2
import numpy as np
import contour  # Other written file - contains code that works with contour-finding and polynomial approximation


def show_image(figure_name, img):
    cv2.imshow(figure_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def resize_image(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def plot_point(img, x, y, color=True):
    if color:
        cv2.circle(img, (x, y), radius=2, color=(0, 0, 255), thickness=-1)
    else:
        cv2.circle(img, (x, y), radius=2, color=(255, 0, 0), thickness=-1)


def plot_parabola(img, polynomial):
    for x in range(len(img[1])):
        y = polynomial[0] + (polynomial[1] * x) + (polynomial[2] * (x ** 2))
        plot_point(img, int(x), int(y), True)


# Transformation derived from https://www.researchgate.net/publication/320303343_Indexing_of_Historical_Document_Images_Ad_Hoc_Dewarping_Technique_for_Handwritten_Text
def remap_point(point, top, top_poly, bottom_poly, top_arc, width, height):
    x, y = point[0], point[1]

    # Points on parabolas corresponding to arbitrary point K
    T = (x, top_poly[0] + (top_poly[1]*x) + (top_poly[2]*x*x))
    G = (x, bottom_poly[0] + (bottom_poly[1]*x) + (bottom_poly[2]*x*x))

    if y < T[1] or y > G[1]:
        return 0, 0

    # Additional desired arc lengths
    at = contour.arc_length(top_poly, T[0])
    tk = abs(T[1] - point[1])
    tg = abs(T[1] - G[1])

    # Apply transformation equations
    new_x = (width * (at/top_arc)) # + top[0][0]
    new_y = (height * (tk/tg)) # + top[0][1]

    return new_x, new_y


# Check out https://docs.opencv.org/3.4/d1/da0/tutorial_remap.html
def transform_image(img):
    a_contour = contour.find_contours(img)
    top, bottom = contour.find_top_bottom_sides(img, a_contour)

    show_image('contour', img)  # For testing purposes
    bounds = top + bottom  # For testing purposes
    for point in bounds:  # For testing purposes
        plot_point(img, point[0], point[1], False)  # For testing purposes
    show_image('bounds', img)  # For testing purposes

    # Find straight bounding rectangle for image dimensions
    a, b, w, h = cv2.boundingRect(a_contour)
    ul, ur, ll, lr = (a, b), (a + w, b), (a, b + h), (a + h, b + h)

    # Crop img to mapping portion
    cropped_img = img[ul[1]:ll[1], ul[0]:ur[0]]

    map_x = np.zeros(shape=(cropped_img.shape[0], cropped_img.shape[1]), dtype=np.float32)
    map_y = np.zeros(shape=(cropped_img.shape[0], cropped_img.shape[1]), dtype=np.float32)

    # Calculations for remap_point
    top_poly = contour.find_polynomial_fit(top)
    bottom_poly = contour.find_polynomial_fit(bottom)
    top_poly[0] -= ul[1]
    bottom_poly[0] -= ul[1]

    plot_parabola(img, top_poly)  # For testing purposes
    plot_parabola(img, bottom_poly)  # For testing purposes
    show_image('paras', img) # For testing purposes

    # Arc lengths of parabola fits
    top_arc = contour.arc_length(top_poly, top[-1][0])

    # Width and height of desired rectangle mapping
    width = map_x.shape[1]
    height = map_x.shape[0]

    # Update maps with remap_point()
    for i in range(height):
        for j in range(width):
            point = (j, i)
            map_x[i, j], map_y[i, j] = remap_point(point=point, top=top, top_poly=top_poly, bottom_poly=bottom_poly, top_arc=top_arc, width=width, height=height)
            # map_x[i, j], map_y[i, j] = remap_point(point=point, width=width, height=height)

    # For speed reasons
    map_x, map_y = cv2.convertMaps(map_x, map_y, dstmap1type=cv2.CV_16SC2)

    # Use cv2.remap() with map_x and map_y
    dst = cv2.remap(cropped_img, map_x, map_y, cv2.INTER_LINEAR)
    return dst


if __name__ == '__main__':
    filepath = '../images/pill_thing.jpg'
    img = cv2.imread(filepath)
    img = img[920: 2600, 1250: 3000]
    # img = cv2.cvtColor(cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)[1],cv2.COLOR_GRAY2BGR)
    show_image('orig', img)
    # cv2.imwrite('origthing.jpg', img)
    plz = transform_image(resize_image(img, 20))
    cv2.imwrite('transformedthing.jpg', plz)
    show_image('plz', plz)

    # FDA
    '''
    for i in range(4, 5):
        filepath = f"images/fda{i}.jpg"
        img = cv2.imread(filepath)
        # Shift viewing frame of images to center on message
        img = img[1500 + (90 * (i - 1)):2000 + (90 * (i - 1)), 600:1500]
        img = cv2.cvtColor(cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 150, 255, cv2.THRESH_BINARY)[1],
                           cv2.COLOR_GRAY2BGR)
        show_image('orig', img)
        cv2.imwrite('orig.jpg', img)
        plz = transform_image(img)
        cv2.imwrite('transformed.jpg', plz)
        show_image('plz', plz)
    '''
