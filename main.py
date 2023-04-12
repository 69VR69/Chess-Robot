import os

import serial
from Computer_Vision.fen_generator import get_fen_from_image
import tensorflow
from camera import Camera


port = 'COM3'

# Débit de transmission carte Arduino
baud_rate = 9600

# Ouvrir une connexion série
# ser = serial.Serial(port, baud_rate)

# Attendre que la connexion soit établie
# ser.flushInput()

possible_inputs = ['de', 'te', 'fe', 'ce', 'e']

project_path = os.getcwd()

if __name__ == '__main__':
    camera = Camera(1)
    # while True:
        # Lire une ligne de données depuis le port série
        # line = ser.readline().decode('utf-8').rstrip()
        # if line in possible_inputs:
            # print(line)
            # print(project_path)
            # camera.take_photo(project_path + "/photo.jpg")
            # pass


