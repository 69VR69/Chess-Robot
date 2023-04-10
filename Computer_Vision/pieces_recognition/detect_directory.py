import glob
import os

from keras.models import load_model

imgWidth = 256
imgHeight = 256

# the names of the classes should be sorted


classes = ["Bishop","Empty", "King", "Knight", "Pawn", "Queen", "Rook"]

import pandas as pd
import numpy as np
# from keras.preprocessing.image import load_img , img_to_array
from keras.utils import load_img, img_to_array
# import load image from keras
import cv2
import h5py
import tensorflow as tf
from keras.applications.vgg16 import VGG16

project_path = os.getcwd()

# model = VGG16(weights=None)
# model.load_weights(project_path + r"/ressources/models/model_VGG16_50epo.h5")
squares_path = project_path + "/board_detection_/test/squares"


def prepareImage(pathToImage):
    image = load_img(pathToImage, target_size=(imgHeight, imgWidth))
    imgResult = img_to_array(image)
    imgResult = np.expand_dims(imgResult, axis=0)
    imgResult = imgResult / 255.
    return imgResult

#
# def predict_all_images_in_directory():
#     files = glob.glob(squares_path + '/*.*')
#     model = load_model(project_path + "/ressources/models/model_7_classes_2.h5")
#     predictions = []
#     for f in files:
#         print(f)
#         imageForModel = prepareImage(f)
#         print(imageForModel.shape)
#         # prediction
#         resultArray = model.predict(imageForModel, batch_size=20, verbose=1)
#         answer = np.argmax(resultArray, axis=1)
#         print(answer[0])
#         predictions.append(answer[0])
#         text = classes[answer[0]]
#         print('Predicted : ' + text + ' for ' + f)
#     return predictions

def predict_all_images_in_directory():
    files = glob.glob(squares_path + '/*.*')
    model = load_model(project_path + "/ressources/models/chess_best_model_new_dataset_7_classes.h5")
    predictions = []
    for i in range(8):
        for j in range(8):
            path = squares_path + "/cropped_" + str(j) + "_" + str(i) + ".jpg"
            imageForModel = prepareImage(path)
            print(imageForModel.shape)
            # prediction
            resultArray = model.predict(imageForModel, batch_size=20, verbose=1)
            answer = np.argmax(resultArray, axis=1)
            print(answer[0])
            predictions.append(answer[0])
            text = classes[answer[0]]
            print('Predicted : ' + text + ' for ' + path)
    return predictions