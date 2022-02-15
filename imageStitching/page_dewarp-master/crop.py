import sys
import cv2


def crop(img):
    x_lower = 0
    x_upper = img.shape[1]
    y_lower = 0
    y_upper = img.shape[0]
    crop_mode = 1
    while True:
        if crop_mode == 1:
            x_lower += 50
        elif crop_mode == 2:
            x_upper -= 50
        elif crop_mode == 3:
            y_lower += 50
        elif crop_mode == 4:
            y_upper -= 50
        new_img = img[y_lower:y_upper, x_lower:x_upper]
        cv2.imshow('crop', new_img)
        if cv2.waitKey(0) == ord('q'):
            crop_mode += 1
            if crop_mode > 4:
                return img[y_lower:y_upper, x_lower:x_upper]
        cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No image input!")
    else:
        filepath = sys.argv[1]
        img = cv2.imread(filepath)
        cv2.imshow("orig", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        low_x, high_x, low_y, high_y = crop(img)
        print("img[", low_y, ":", high_y, ",", low_x, ":", high_x, "]")