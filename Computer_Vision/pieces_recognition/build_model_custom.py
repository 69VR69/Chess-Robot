# Create the CNN model
import os

from keras.layers import BatchNormalization
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
from glob import glob
import tensorflow as tf

imgWidth = 256
imgHeight = 256
batchSize = 64
numOfEpochs = 50

project_path = os.getcwd().replace("Computer_Vision/pieces_recognition", "")
print(project_path)
# TRAINING_DIR = "C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train3"
TRAINING_DIR = project_path + "/Computer_Vision/ressources/dataset/train3"

# NumOfClasses = len(glob('C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset/train3/*')) # /*
NumOfClasses = len(glob(project_path + '/Computer_Vision/ressources/dataset/train3/*'))  # /*

print("taille :")
print(NumOfClasses)  # 7 classes
# os.listdir("C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/dataset")
os.listdir(project_path + "/Computer_Vision/ressources/dataset")
# data augmentation to increase the train data

# data augmentation, pour avoir plus d'images d'entrainement
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
validation_DIR = project_path + "/Computer_Vision/ressources/dataset/validation3"
val_datagen = ImageDataGenerator(rescale=1 / 255.0)

val_generator = val_datagen.flow_from_directory(validation_DIR,
                                                batch_size=batchSize,
                                                class_mode='categorical',
                                                target_size=(imgHeight, imgWidth))

# early stopping

callBack = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='auto')

# if we will find a better model we will save it here :
# bestModelFileName = "C:/Users/ddbtn/PycharmProjects/Chess-Robot/Computer_Vision/ressources/models/chess_best_model_new_dataset.h5"
bestModelFileName = project_path + "/Computer_Vision/ressources/models/model_7_classes_2.h5"

bestModel = ModelCheckpoint(bestModelFileName, monitor='val_accuracy', verbose=1, save_best_only=True)

# the model :
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(imgHeight, imgWidth, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(256, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),

    Dense(512, activation='relu'),
    # Dense(512, activation='relu'),

    Dense(NumOfClasses, activation='softmax')
    # softmax -> 0 to 1 => softmax = version améliorer de sogmoid = pour 2 classes

])
# model.add(Dense(6, activation = "softmax"))
# reg = keras.regularizers.l2(0.0005)
# model = keras.Sequential()
# model.add(
#     Conv2D(32, (3, 3), padding="same", activation='relu', input_shape=(imgHeight, imgWidth, 3), kernel_regularizer=reg))
# model.add(MaxPooling2D(pool_size=(2, 2))) # this means that we will use a 2x2 pooling filter, it is used to reduce the size of the image
# # model.add(BatchNormalization(axis=3))
# # model.add(Dropout(0.25))
#
# model.add(Conv2D(64, (3, 3), padding="same", activation="relu", kernel_regularizer=reg))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# # model.add(BatchNormalization(axis=3))
# # model.add(Dropout(0.25))
#
# model.add(Conv2D(128, (3, 3), padding="same", activation="relu", kernel_regularizer=reg))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# # model.add(BatchNormalization(axis=3))
# model.add(Dropout(0.25)) # this means that 25% of the neurons will be randomly dropped during training
#
# model.add(Flatten()) # this converts our 3D feature maps to 1D feature vectors
# model.add(Dense(128, activation='relu'))
# model.add(BatchNormalization()) # this is used to normalize the activations of the previous layer at each batch
# model.add(Dropout(0.5))
# model.add(Dense(NumOfClasses, activation='softmax'))

print(model.summary())

# compile the model with Adam optimizer

# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(train_generator,
                    epochs=numOfEpochs,
                    verbose=1,
                    validation_data=val_generator,
                    callbacks=[bestModel])

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
