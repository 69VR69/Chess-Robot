# int main(int argc, char** argv)
# {
#     // Reading the images
#     cv::Mat img = cv::imread("chessboard_2.jpg", cv::IMREAD_GRAYSCALE);
#     cv::Mat img_rgb = cv::imread("chessboard_2.jpg", cv::IMREAD_COLOR);
#     cv::Mat bilateral_filtered_image;
#
#     // Applying a bilateral filter to smooth the image
#     cv::bilateralFilter(img, bilateral_filtered_image, 5, 75, 75);
#     cv::namedWindow("Bilateral Filter", cv::WINDOW_NORMAL);
#     cv::imshow("Bilateral Filter", bilateral_filtered_image);
#     cv::waitKey(0);
#
#     // Find corner points using goodFeaturestoTrack with appropriate parameters
#     std::vector<cv::Point2f> corners;
#     cv::goodFeaturesToTrack(bilateral_filtered_image, corners, 200, 0.01, 120);
#     std::cout << corners.size() << std::endl;
#
#     // Draw all corners on the original image and show the image
#     for (size_t i = 0; i < corners.size(); ++i) {
#         cv::circle(img_rgb, cv::Point2f(corners[i].x, corners[i].y), 7, (0,0,255), 3);
#     }
#     cv::namedWindow("Corners", cv::WINDOW_NORMAL);
#     cv::imshow("Corners", img_rgb);
#     cv::waitKey(0);
# }


# convert above code to python
import cv2 as cv
import numpy as np

# img = cv.imread("./test/aaaaa.jpg", cv.IMREAD_GRAYSCALE)
# img_rgb = cv.imread("./test/aaaaa.jpg", cv.IMREAD_COLOR)
# bilateral_filtered_image = cv.bilateralFilter(img, 5, 75, 75)
# cv.namedWindow("Bilateral Filter", cv.WINDOW_NORMAL)
# cv.imshow("Bilateral Filter", bilateral_filtered_image)
# cv.waitKey(0)
# corners = cv.goodFeaturesToTrack(bilateral_filtered_image, 200, 0.01, 120)
# print(corners.size)
# # print(corners[0][0][1])
# for i in range(int(corners.size/2)):
#     cv.circle(img_rgb, (int(corners[i][0][0]), int(corners[i][0][1])), 7, (0, 0, 255), 3)
#
# cv.namedWindow("Corners", cv.WINDOW_NORMAL)
# cv.imshow("Corners", img_rgb)
# cv.waitKey(0)

# import cv2
# import numpy as np
#
# # Charger l'image du plateau d'échecs
# img = cv2.imread('./test/J5wZn.jpg')
#
# # Convertir l'image en niveaux de gris
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Appliquer un seuillage pour mettre en évidence les contours des cases
# thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)[1]
#
# # Trouver les contours des cases sur le plateau
# contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours = contours[0] if len(contours) == 2 else contours[1]
#
# # Définir la taille des images de chaque case
# tile_size = (200, 200)
#
# # Pour chaque contour trouvé, générer une image de la case correspondante
# for contour in contours:
#     # Calculer les coordonnées du rectangle entourant la case
#     x, y, w, h = cv2.boundingRect(contour)
#
#     # Extraire l'image de la case du plateau d'échecs
#     tile = img[y:y+h, x:x+w]
#
#     # Redimensionner l'image de la case à la taille souhaitée
#     tile = cv2.resize(tile, tile_size)
#
#     # Enregistrer l'image de la case dans un fichier
#     cv2.imwrite('tile_{}.jpg'.format(x + y), tile)
#     print("aX")



import cv2

import numpy as np

# Charger l'image du plateau d'échecs
img = cv2.imread('./test/J5wZn.jpg') #TODO 14/12/2022

# Convertir l'image en niveaux de gris
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Appliquer un filtre gaussien pour éliminer le bruit
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Appliquer un seuillage adaptatif pour mettre en évidence les contours des cases
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# Trouver les contours des cases sur le plateau
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

# Définir la taille des images de chaque case
tile_size = (200, 200)

# Pour chaque contour trouvé, générer une image de la case correspondante
for contour in contours:
    # Calculer les coordonnées du rectangle entourant la case
    x, y, w, h = cv2.boundingRect(contour)

    # Extraire l'image de la case du plateau d'échecs
    tile = img[y:y+h, x:x+w]

    # Redimensionner l'image de la case à la taille souhaitée
    tile = cv2.resize(tile, tile_size)

    # Enregistrer l'image de la case dans un fichier
    cv2.imwrite('tile_{}.jpg'.format(x + y), tile)
