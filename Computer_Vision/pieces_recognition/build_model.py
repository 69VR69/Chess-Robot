# Create the CNN model
import os

from keras import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
from glob import glob
import tensorflow as tf



# imgWidth = 256
# imgHeight = 256
imgWidth = 224
imgHeight = 224
batchSize = 32
numOfEpochs = 50

# TRAINING_DIR = "C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train3"
TRAINING_DIR = "/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train3"

# NumOfClasses = len(glob('C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train3/*')) # /*
NumOfClasses = len(glob('/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train3/*'))  # /*

print("taille :")
print(NumOfClasses)  # 6 classes
# os.listdir("C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset")
os.listdir("/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset")
# data augmentation to increase the train data

#data augmentation, pour avoir plus d'images d'entrainement
train_datagen = ImageDataGenerator(rescale=1 / 255.0,  # normalize between 0 - 1
                                   rotation_range=30,
                                   zoom_range=0.4,
                                   horizontal_flip=True,
                                   shear_range=0.4)

# load the data
train_generator = train_datagen.flow_from_directory(TRAINING_DIR,
                                                    batch_size=batchSize,
                                                    class_mode='categorical',
                                                    target_size=(imgHeight, imgWidth))

# validation_DIR = "C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/validation3"
validation_DIR = "/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/validation3"
val_datagen = ImageDataGenerator(rescale=1 / 255.0)

val_generator = val_datagen.flow_from_directory(validation_DIR,
                                                batch_size=batchSize,
                                                class_mode='categorical',
                                                target_size=(imgHeight, imgWidth))

# early stopping

callBack = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='auto')

# if we will find a better model we will save it here :
# bestModelFileName = "C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/chess_best_model_new_dataset.h5"
bestModelFileName = "/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/chess_best_model_new_dataset.h5"

bestModel = ModelCheckpoint(bestModelFileName, monitor='val_accuracy', verbose=1, save_best_only=True)

# the model :

# model = Sequential([
#     Conv2D(32, (3, 3), activation='relu', input_shape=(imgHeight, imgWidth, 3)),
#     MaxPooling2D(2, 2),
#
#     Conv2D(64, (3, 3), activation='relu'),
#     MaxPooling2D(2, 2),
#
#     # Conv2D(64, (3, 3), activation='relu'),
#     # MaxPooling2D(2, 2),
#
#     Conv2D(128, (3, 3), activation='relu'),
#     MaxPooling2D(2, 2),
#
#     Conv2D(256, (3, 3), activation='relu'),
#     MaxPooling2D(2, 2),
#
#     Flatten(),
#
#     Dense(512, activation='relu'),
#     Dense(512, activation='relu'),
#
#     Dense(NumOfClasses, activation='softmax')  # softmax -> 0 to 1 => softmax = version améliorer de sogmoid = pour 2 classes
#
# ])
# model.add(Dense(6, activation = "softmax"))


# print(model.summary())

# compile the model with Adam optimizer

# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])


# test using existing model
from keras.applications.vgg16 import VGG16
from keras.applications.imagenet_utils import decode_predictions

model = VGG16(weights='imagenet')
model.summary()

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze convolutional layers
for layer in base_model.layers:
    layer.trainable = False

# Establish new fully connected block
x = base_model.output
x = Flatten()(x)  # flatten from convolution tensor output
x = Dense(500, activation='relu')(x)  # number of layers and units are hyperparameters, as usual
x = Dense(500, activation='relu')(x)
predictions = Dense(6, activation='softmax')(x)  # should match # of classes predicted

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)
# model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])



# history = model.fit(train_generator,
#                     epochs=numOfEpochs,
#                     verbose=1,
#                     validation_data=val_generator,
#                     callbacks=[bestModel])
history = model.fit(train_generator,
                    epochs=numOfEpochs,
                    verbose=1,
                    validation_data=val_generator)
model.save_weights('/mnt/c/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/model_VGG16_50epo.h5')

# display the result using pyplot

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))  # for the max value in the diagram

# accuracy chart

fig = plt.figure(figsize=(14, 7))
plt.plot(epochs, acc, 'r', label="Train accuracy")
plt.plot(epochs, val_acc, 'b', label="Validation accuracy")
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Train and validation accuracy')
plt.legend(loc='lower right')
plt.show()

# loss chart
fig2 = plt.figure(figsize=(14, 7))
plt.plot(epochs, loss, 'r', label="Train loss")
plt.plot(epochs, val_loss, 'b', label="Validation loss")
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Train and validation Loss')
plt.legend(loc='upper right')
plt.show()
