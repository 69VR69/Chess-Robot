import cv2


# class Camera:
#     def __init__(self, index=0):
#         self.cap = cv2.VideoCapture(index)
#
#     def take_photo(self, filename="photo.jpg"):
#         ret, frame = self.cap.read()
#         if ret:
#             cv2.imwrite(filename, frame)
#         else:
#             print("Error: Can't take photo")
#         return frame
#
#     def __del__(self):
#         self.cap.release()


# Ouvrir la caméra
cap = cv2.VideoCapture(1) # todo => changer d'index pour la camera externe

# Lire un cadre de la caméra
ret, frame = cap.read()

# Enregistrer l'image
cv2.imwrite("photo.jpg", frame)

# Libérer la caméraq
cap.release()

# Afficher l'image
cv2.imshow("Photo", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
