import cv2
import numpy as np


# image2 -> the image of the dustbin before throwing in the new garbage(object of interest)
# image1 -> the image of the dustbin after throwing in the new garbage(object of interest)
# plz click images from a steady camera, else the algo wont work

def pre_processing(newImg=None, prevImg=None):
    try:
        img = cv2.imread(prevImg)
        img2 = cv2.imread(newImg)
        if img == img2:
            cv2.imwrite('send_to_vision.jpg', img2)
        rowst, colst, channel = img.shape
        for rows in range(rowst):
            for cols in range(colst):
                # tcount += 1
                val1 = float(abs(int(img[rows, cols, 0]) - int(img2[rows, cols, 0])))
                val2 = float(abs(int(img[rows, cols, 1]) - int(img2[rows, cols, 1])))
                val3 = float(abs(int(img[rows, cols, 2]) - int(img2[rows, cols, 2])))
                dist = np.sqrt(val1 * val1 + val2 * val2 + val3 * val3)

                if dist <= 45:
                    img2[rows, cols] = [180, 130, 210]

        lu = np.zeros([2])
        lu[0] = 480
        lu[1] = 640
        rl = np.zeros([2])
        rl[0] = 0
        rl[1] = 0

        for i in range(0, rowst, 20):
            for j in range(0, colst, 20):
                count = 0
                for p in range(i, i + 20, 1):
                    for q in range(j, j + 20, 1):
                        if img2[p, q, 0] == 180 and img2[p, q, 1] == 130 and img2[p, q, 2] == 210:
                            count += 1
                if count < 120:
                    lu[0] = min(lu[0], i)
                    lu[1] = min(lu[1], j)

                    rl[0] = max(rl[0], i)
                    rl[1] = max(rl[1], j)

                    img2[i, j] = [255, 255, 255]

        if lu[0] - 80 >= 0:
            lu[0] -= 80
        elif lu[0] - 60 >= 0:
            lu[0] -= 60
        elif lu[0] - 40 >= 0:
            lu[0] -= 40

        if lu[1] - 80 >= 0:
            lu[1] -= 80
        elif lu[1] - 60 >= 0:
            lu[1] -= 60
        elif lu[1] - 40 >= 0:
            lu[1] -= 40

        if rl[0] + 80 < 480:
            rl[0] += 80
        elif rl[0] + 60 < 480:
            rl[0] += 60
        elif rl[0] + 40 < 480:
            rl[0] += 40

        if rl[1] + 80 < 640:
            rl[1] += 80
        elif rl[1] + 60 < 640:
            rl[1] += 60
        elif rl[1] + 40 < 640:
            rl[1] += 40

        img2 = img2[int(lu[0]):int(rl[0]), int(lu[1]):int(rl[1])]
        cv2.imwrite("send_to_vision.jpg", img2)
        print("image generated")
    except:
        cv2.imwrite('send_to_vision.jpg', cv2.imread(newImg))
