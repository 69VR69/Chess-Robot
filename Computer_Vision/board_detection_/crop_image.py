import cv2
import matplotlib.pyplot as plt
import numpy as np
# from skimage.filters import threshold_otsu
import os
import glob


# Round to next smaller multiple of 8
# https://www.geeksforgeeks.org/round-to-next-smaller-multiple-of-8/
def round_down_to_next_multiple_of_8(a):
    return a & (-8)


# Read image, and shrink to quadratic shape with width and height of
# next smaller multiple of 8
# img = cv2.imread(r'C:\Users\ddbtn\PycharmProjects\neural-chessboard-y - Copie\test\test1_cropped.jpg')

def create_cells(img_path):
    img = cv2.imread(img_path)
    wh = np.min(round_down_to_next_multiple_of_8(np.array(img.shape[:2])))
    img = cv2.resize(img, (wh, wh))

    # Prepare some visualization output
    # out = img.copy()
    # plt.figure(1, figsize=(18, 6))
    # plt.subplot(1, 3, 1), plt.imshow(img)

    # Blur image
    # img = cv2.blur(img, (5, 5))

    # path = r'C:\Users\ddbtn\PycharmProjects\Chess-Robot\Computer_Vision\board_detection\test\squares'
    directory = os.getcwd()
    squares_path = directory + "/board_detection_/test/squares"
    files = glob.glob(squares_path + '/*.*')
    print(squares_path)
    # print(files)
    for f in files:
        os.remove(f)

    # Iterate tiles, and count unique colors inside
    # https://stackoverflow.com/a/56606457/11089932
    wh_t = wh // 8
    # count_unique_colors = np.zeros((8, 8))
    # for x in np.arange(8):
    #     for y in np.arange(8):
    #         tile = img[y * wh_t:(y + 1) * wh_t, x * wh_t:(x + 1) * wh_t]
    #         tile = tile[3:-3, 3:-3]
    #         count_unique_colors[y, x] = np.unique(tile.reshape(-1, tile.shape[-1]), axis=0).shape[0]

    # Mask empty squares using cutoff from Otsu's method
    # val = threshold_otsu(count_unique_colors)
    # print(val)
    # mask = count_unique_colors < val
    # print(mask)
    # Some more visualization output


    for x in np.arange(8):
        for y in np.arange(8):
            # if mask[y, x]:
            #     cv2.rectangle(out, (x * wh_t + 3, y * wh_t + 3),
            #                   ((x + 1) * wh_t - 3, (y + 1) * wh_t - 3), (0, 255, 0), 2)
            #     # save image with coordinates of the square
            # else:
            #     cv2.rectangle(out, (x * wh_t + 3, y * wh_t + 3),
            #                   ((x + 1) * wh_t - 3, (y + 1) * wh_t - 3), (255, 0, 0), 2)
            cv2.imwrite(squares_path + '/cropped_' +
                        str(x) + '_' + str(y) + '.jpg', img[y * wh_t:(y + 1) * wh_t, x * wh_t:(x + 1) * wh_t])

    # plt.subplot(1, 3, 2), plt.imshow(count_unique_colors, cmap='gray')
    # plt.subplot(1, 3, 3), plt.imshow(out)
    # plt.tight_layout(), plt.show()
    return True

