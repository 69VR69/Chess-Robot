import os
import fen_functions as fen_functions
import numpy as np

chesspieces = {
    0: "B",
    2: "K",
    3: "N",
    4: "P",
    5: "Q",
    6: "R",
}

def get_fen_from_image(path_captured_image):
    # image_path = fen_gen.get_chessboard_img_cropped(r"./board_detection_/test/in/cc10.jpg")
    image_path = fen_functions.get_chessboard_img_cropped(path_captured_image)
    # todo attention au sens du plateau => blanc en haut (position cam)
    print(image_path)
    is_ok = fen_functions.create_cells_from_image(image_path)
    print(is_ok)
    project_path = os.getcwd()

    if is_ok:
        print("Détection des pièces ...")
        predictions = fen_functions.create_matrix_from_cells()
        print(predictions)
        matrix = np.reshape(predictions, (8, 8))
        # matrix = np.rot90(matrix, k=1, axes=(0, 1))

        print(matrix)
        # read the matrix line by line and create the fen string
        fen = ""
        for i in range(8):
            empty = 0
            for j in range(8):
                if matrix[i][j] == 1:
                    empty += 1
                else:
                    if empty != 0:
                        fen += str(empty)
                        empty = 0
                    fen += str(chesspieces[matrix[i][j]])
            if empty != 0:
                fen += str(empty)
            if i != 7:
                fen += "/"

    else:
        print("Erreur lors du crop du chessboard")
    print(fen)
    return fen