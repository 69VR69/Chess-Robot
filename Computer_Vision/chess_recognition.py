# import cv2 as cv
# from PIL import Image
# import os, glob
# import chess.pgn
#
#
# #TODO essayer de bien detecter les cases, centrer sur la photo sur le board unqiuement, une fois ça
# #TODO essayer de découper l'image crop en 64 case et détecter la couleur et la pièce
# def t(path):
#     #grayscale
#     img = cv.imread(path, 0)
#     blur = cv.GaussianBlur(img, (7, 7), 2)
#     # _ : stocke le résultat de l'opération du dessus
#     _, img_binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
#     im_res = Image.fromarray(img_binary)
#     im_res.save("test.png")
#     img_edge = cv.Canny(img_binary, 50, 50)  # we use the canny function to edge canny the image.
#     cv.imshow('t', img_edge)  #
#     cv.waitKey(0)
#
#     # read the game file and set board
#     pgn = open("./ressources/gencupp22.pgn")
#     game = chess.pgn.read_game(pgn)
#     board = game.board()
#     print(board)
#
#     #code a chess recognition pieces with an image in input usign a CNN
#
#     #code a loop
#
#     # read chessboard image at move x, jump board to move x
#     filename = "move_x.jpg"
#     move = game.mainline_moves()
#     # board.push(move)
#
#     for i in range(64):
#         piece = board.piece_at(i)
#         if piece is None:
#         # save image with empty label
#             print("Non")
#         else:
#             print(piece.symbol())
#             # piece.
#
#     # save image with piece.symbol() label
