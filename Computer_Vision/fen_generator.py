import board_detection_.main as bd
import board_detection_.crop_image as cropper
import pieces_recognition.detect_directory as detect


def get_chessboard_img_cropped(path_captured_image):
    return bd.detect(path_captured_image)


def create_cells_from_image(path_cropped_image):
    return cropper.create_cells(path_cropped_image)


def create_matrix_from_cells():
    return detect.predict_all_images_in_directory()

# path = get_chessboard_img_cropped(r"./board_detection/test/in/3.jpg")
# print(path)
