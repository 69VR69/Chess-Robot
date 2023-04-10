from keras.models import load_model

imgWidth = 224
imgHeight = 224

# the names of the classes should be sorted


classes = ["Bishop", "King", "Knight", "Pawn", "Queen", "Rook"]

import pandas as pd
import numpy as np
# from keras.preprocessing.image import load_img , img_to_array
from keras.utils import load_img, img_to_array
# import load image from keras
import cv2
import h5py

# lets load the model
import tensorflow as tf

# model = load_model(r"/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/model_VGG16_50epo.h5")
# model = load_model(r"/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/model_VGG16_50epo.h5")
# print(model.summary() )
from keras.applications.vgg16 import VGG16

model = VGG16(weights=None)
model.load_weights(
    r"/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/model_VGG16_50epo.h5")


# lets build a function for preparing an image for model

def prepareImage(pathToImage):
    image = load_img(pathToImage, target_size=(imgHeight, imgWidth))
    imgResult = img_to_array(image)
    imgResult = np.expand_dims(imgResult, axis=0)
    imgResult = imgResult / 224.
    return imgResult


# testImagePath = r"/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/validation3/Bishop/555.jpg"
# testImagePath = r"/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train2/king_w/test1_cropped_4_7.jpg"
testImagePath = r"/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train2/queen_w/test1_cropped_3_7.jpg"

# run the function
imageForModel = prepareImage(testImagePath)

print(imageForModel.shape)

# predict the image
resultArray = model.predict(imageForModel, batch_size=20, verbose=1)
answer = np.argmax(resultArray, axis=1)

print(answer[0])

text = classes[answer[0]]
print('Predicted : ' + text)

# lets show the image with the predicted text

img = cv2.imread(testImagePath)
font = cv2.FONT_HERSHEY_COMPLEX

cv2.putText(img, text, (0, 100), font, 2, (209, 19, 77), 3)
cv2.imshow('img', img)
cv2.waitKey(0)
