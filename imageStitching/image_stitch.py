# Read command-line arguments
# Incremental stitching, catch failure cases

import cv2
import sys


def attempt_stitch(img1, img2):
    stitcher = cv2.Stitcher_create()
    try:
        stitched, status = stitcher.stitch([img1, img2])
    except:
        return None

    if stitched == 0:
        return status
    else:
        return None


def stitch_implemented(imgs):
    stitcher = cv2.Stitcher_create()
    stitched, status = stitcher.stitch(imgs)
    print(stitched)
    if stitched == 0:
        return status
    else:
        return None


def stitch_recursive(imgs):
    if len(imgs) == 1:
        print("Stitching complete")
        return imgs

    stitched_imgs = []

    while len(imgs) > 1:
        print("Attempting to stitch...")
        temp_img = attempt_stitch(imgs[0], imgs[1])
        if temp_img is not None:
            print("Stitch succeeded, moving on...")
            stitched_imgs.append(temp_img)
            imgs.pop(0)
            imgs.pop(0)
            if len(imgs) == 1:
                stitched_imgs.append(imgs.pop(0))
        else:
            print("Stitch failed, moving on...")
            stitched_imgs.append(imgs.pop(1))

    print("Next iteration..., list length", len(stitched_imgs))
    print("")
    return stitch_recursive(stitched_imgs)


# Iterative method for sequential image stitching
def stitch_stack(imgs):
    if len(imgs) == 1:
        print("Stitching complete.")
        return imgs

    next_stack = []
    while len(imgs) > 1:
        print("\nNext iteration, list length", len(imgs), "\n")
        while len(imgs) > 1:
            print("Attempting to stitch...")
            temp_img = attempt_stitch(imgs[0], imgs[1])
            if temp_img is not None:
                print("Stitch succeeded, moving on...")
                next_stack.append(temp_img)
                imgs.pop(0)
                imgs.pop(0)
                if len(imgs) == 1:
                    next_stack.append(imgs.pop(0))
            else:
                print("Stitch failed, moving on...")
                next_stack.append(imgs.pop(1))
        imgs = next_stack
        next_stack = []
    return imgs


def main():
    images = []
    if len(sys.argv) < 2:
        print("No images input!")
        images = [cv2.imread(f"IMG_{i}.JPG") for i in range(5135, 5145)]  # do NOT use a large range of images
    else:
        images = [cv2.imread(file) for file in sys.argv[1:]]
    # img = stitch_recursive(images)[0]
    # img = stitch_implemented(images)
    img = stitch_stack(images)[0]
    # cv2.imwrite("StitchRecursive.jpg", img)
    cv2.imshow("Stitched", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
