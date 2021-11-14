import cv2
import pytesseract
import difflib


def main():
    img1 = cv2.imread('label1.jpg')
    img2 = cv2.imread('label2.jpg')

    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    printed1 = pytesseract.image_to_string(img1, config=custom_config)
    printed2 = pytesseract.image_to_string(img2, config=custom_config)
    print(printed1)
    print(printed2)

    lines1 = printed1.splitlines()
    lines2 = printed2.splitlines()

    print("Part 1:")
    print(lines1[0])
    print("")
    print("Part 2:")
    print(lines2[0])
    print("")
    s = difflib.SequenceMatcher(None, lines1[0], lines2[0])
    pos_a, pos_b, size = s.find_longest_match(0, len(lines1[0]), 0, len(lines2[0]))

    concat = lines1[0][0:pos_a + size] + lines2[0][pos_b + size: len(lines2[0])]
    print("Concatenated:")
    print(concat)

    print("")
    print("Real text:")
    print("Uses for relief of occasional sleeplesness when associated")



if __name__ == '__main__':
    main()
