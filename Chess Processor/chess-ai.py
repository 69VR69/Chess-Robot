import datetime

from stockfish import Stockfish

log_game = True

stockfish = Stockfish('stockfish_15_win_x64_popcnt/stockfish_15_win_x64_popcnt/stockfish_15_x64_popcnt.exe')
listMoves = []

pieces = {
    "P": "Pawn",  # pion
    "N": "Knight",  # cavalier
    "B": "Bishop",  # fou
    "R": "Rook",  # tour
    "Q": "Queen",  # reine
    "K": "King"  # roi
}


class Piece:
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.color = color

    def __str__(self):
        return self.name + " " + self.position + " " + self.color


colorTurn = "w"
castlingRights = "-"
en_passant = "-"
half_move_clock = 0
full_move_number = 1

listPieces = {
    1: Piece("R", "a1", "w"), 2: Piece("N", "b1", "w"), 3: Piece("B", "c1", "w"), 4: Piece("Q", "d1", "w"),
    5: Piece("K", "e1", "w"), 6: Piece("B", "f1", "w"), 7: Piece("N", "g1", "w"), 8: Piece("R", "h1", "w"),
    9: Piece("P", "a2", "w"), 10: Piece("P", "b2", "w"), 11: Piece("P", "c2", "w"), 12: Piece("P", "d2", "w"),
    13: Piece("P", "e2", "w"), 14: Piece("P", "f2", "w"), 15: Piece("P", "g2", "w"), 16: Piece("P", "h2", "w"),
    17: Piece("P", "a7", "b"), 18: Piece("P", "b7", "b"), 19: Piece("P", "c7", "b"), 20: Piece("P", "d7", "b"),
    21: Piece("P", "e7", "b"), 22: Piece("P", "f7", "b"), 23: Piece("P", "g7", "b"), 24: Piece("P", "h7", "b"),
    25: Piece("R", "a8", "b"), 26: Piece("N", "b8", "b"), 27: Piece("B", "c8", "b"), 28: Piece("Q", "d8", "b"),
    29: Piece("K", "e8", "b"), 30: Piece("B", "f8", "b"), 31: Piece("N", "g8", "b"), 32: Piece("R", "h8", "b")
}


# region FEN Manipulation
def compare(fen1, fen2):
    move_played = ""

    splitted_fen1 = fen1.split(" ")
    splitted_fen2 = fen2.split(" ")

    board1 = splitted_fen1[0].split("/", 8)
    board2 = splitted_fen2[0].split("/", 8)

    for i in reversed(range(len(board1))) if splitted_fen2[1].split(" ", 1)[0] != 'w' else range(len(board1)):
        if board1[i] == board2[i]:
            continue
        else:
            s1 = stringify_fen(board1[i])
            s2 = stringify_fen(board2[i])

            for j in range(len(s1)):
                if s1[j] == s2[j]:
                    continue
                else:
                    if s1[j] != "." or s2[j] != ".":
                        move_played += str(chr(97 + j)) + str(8 - i)
    return move_played


def stringify_fen(fen_part):
    result = ""
    if fen_part == "":
        return result
    else:
        for fp in fen_part:
            if fp.isdigit():
                for j in range(int(fp)):
                    result = result + "."
            else:
                result = result + fp
        return result


def init_list_piece_from_fen(fen):
    fen = fen.split(" ")
    fen = fen[0].split("/")
    for i in range(len(fen)):
        for j in range(len(fen[i])):
            if fen[i][j].isalpha():
                listPieces[i + j] = Piece(fen[i][j], chr(97 + j) + str(8 - i), "w" if fen[i][j].isupper() else "b")


def get_piece_id_from_position(position):
    for key, value in listPieces.items():
        if value.position == position:
            return key
    return None


def get_piece_from_position(position):
    piece_id = get_piece_id_from_position(position)
    if piece_id is not None:
        return listPieces[piece_id]
    return None


def update_list_pieces_from_move(move):
    current_piece = get_piece_from_position(move[0:2])
    removed_piece = None
    global half_move_clock
    global full_move_number

    if current_piece is None:
        raise Exception("No piece found at position " + move[0:2])
    else:
        if get_piece_from_position(move[2:4]) is not None:
            removed_piece = get_piece_id_from_position(move[2:4])
            del listPieces[removed_piece]

        current_piece.position = move[2:4]

        if current_piece.name != "P":
            half_move_clock += 1
        else:
            half_move_clock = 0

    return removed_piece


def create_fen_from_list_pieces():
    fen = ""
    empty = 0

    for i in range(8):
        for j in range(8):
            piece = get_piece_from_position(chr(97 + j) + str(8 - i))

            if piece is None:
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                piece_name = piece.name
                fen += piece_name.lower() if piece.color == "b" else piece_name.upper()

        if i < 7:
            if empty > 0:
                fen += str(empty)
                empty = 0
            fen += "/"

    fen += " " + colorTurn + " " + castlingRights + " " + en_passant + " " + str(half_move_clock) + " " + str(
        full_move_number)

    return fen


# endregion FEN Manipulation

# region Game Logic
def is_legal_move(fen, move):
    if len(move) != 4:
        print("Invalid move : not enough characters in move (" + move + ")")
        return False

    if (move[0] < 'A' or move[0] > 'H') or (move[2] < 'A' or move[2] > 'H'):
        if (move[1] < '1' or move[1] > '8') or (move[3] < '1' or move[3] > '8'):
            print("Invalid move : invalid characters")
            return False

    stockfish.set_fen_position(fen)
    return stockfish.is_move_correct(move)


def is_game_over():
    if stockfish.does_current_engine_version_have_wdl_option():
        return stockfish.get_wdl_stats() is None
    else:
        raise Exception("This Stockfish version does not support WDL option so we cannot detect end of game")


def find_next_move(fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()


def detect_promotion(move):
    if move[4:5] == "q":
        promote_pawn(get_piece_id_from_position(move[0:2]), "Q")
    elif move[4:5] == "r":
        promote_pawn(get_piece_id_from_position(move[0:2]), "R")
    elif move[4:5] == "b":
        promote_pawn(get_piece_id_from_position(move[0:2]), "B")
    elif move[4:5] == "n":
        promote_pawn(get_piece_id_from_position(move[0:2]), "N")
    else:
        return


def promote_pawn(id, new_piece):
    if new_piece not in pieces:
        raise Exception("Invalid piece : " + new_piece)
    else:
        listPieces[id].name = new_piece


def generate_message(fen, message):
    prev_move = get_previous_move(fen, False)

    if is_game_over():
        return message + ';' + "Game over"

    if prev_move != '' and not is_legal_move(fen, prev_move):
        return message + ';' + "Illegal move detected : " + prev_move

    return message


def change_turn():
    global colorTurn
    colorTurn = "w" if colorTurn == "b" else "b"


def get_castling_rights():  # TODO
    return castlingRights


def get_en_passant():  # TODO
    return en_passant


# endregion Game Logic

def get_previous_move(fen, add_move):
    prev_move = compare(fen, stockfish.get_fen_position())
    if add_move:
        listMoves.append(prev_move)
    return prev_move


def get_next_move(fen):
    next_move = find_next_move(fen)
    listMoves.append(next_move)
    return next_move


def get_list_moves():
    return listMoves


def reset_game():
    global listMoves
    global listPieces
    global colorTurn
    global castlingRights
    global en_passant
    global half_move_clock
    global full_move_number

    listMoves = []
    listPieces = {
        1: Piece("R", "a1", "w"), 2: Piece("N", "b1", "w"), 3: Piece("B", "c1", "w"), 4: Piece("Q", "d1", "w"),
        5: Piece("K", "e1", "w"), 6: Piece("B", "f1", "w"), 7: Piece("N", "g1", "w"), 8: Piece("R", "h1", "w"),
        9: Piece("P", "a2", "w"), 10: Piece("P", "b2", "w"), 11: Piece("P", "c2", "w"), 12: Piece("P", "d2", "w"),
        13: Piece("P", "e2", "w"), 14: Piece("P", "f2", "w"), 15: Piece("P", "g2", "w"), 16: Piece("P", "h2", "w"),
        17: Piece("P", "a7", "b"), 18: Piece("P", "b7", "b"), 19: Piece("P", "c7", "b"), 20: Piece("P", "d7", "b"),
        21: Piece("P", "e7", "b"), 22: Piece("P", "f7", "b"), 23: Piece("P", "g7", "b"), 24: Piece("P", "h7", "b"),
        25: Piece("R", "a8", "b"), 26: Piece("N", "b8", "b"), 27: Piece("B", "c8", "b"), 28: Piece("Q", "d8", "b"),
        29: Piece("K", "e8", "b"), 30: Piece("B", "f8", "b"), 31: Piece("N", "g8", "b"), 32: Piece("R", "h8", "b")
    }
    colorTurn = "w"
    castlingRights = "-"
    en_passant = "-"
    half_move_clock = 0
    full_move_number = 1

    stockfish.set_fen_position(create_fen_from_list_pieces())


def play_turn(fen):
    global full_move_number

    message = generate_message(fen, "")

    move = get_next_move(fen)
    full_move_number += 1
    detect_promotion(move)
    removed_piece = update_list_pieces_from_move(move)

    piece_to_move = get_piece_from_position(move[0:2])

    return piece_to_move, move, removed_piece, message


def play_solo():
    reset_game()
    fen = stockfish.get_fen_position()
    counter = 0
    delta_sum = 0
    while (not is_game_over()):
        if log_game:
            start = datetime.datetime.now()

        counter += 1
        print("\tTurn " + str(counter))

        play_turn(fen)
        change_turn()
        fen = create_fen_from_list_pieces()
        stockfish.set_fen_position(fen)

        if log_game:
            print(fen)
            print(stockfish.get_board_visual())

            delta = datetime.datetime.now() - start
            delta_sum += delta.total_seconds()
            print("Time : " + str(delta.total_seconds()) + "s")
            mean_delta = delta_sum / counter
            print("Mean time : " + str(mean_delta) + "s")

    return listMoves


# region test
if __name__ == '__main__':
    print('')

    stockfish.set_elo_rating(2000)

    # fen1 = "qbrkbnrn/pppppppp/8/8/8/8/PPPPPPPP/QBRKBNRN w - - 0 1"
    # fen2 = "qbrkbnrn/pppppppp/8/8/8/3P4/PPP1PPPP/QBRKBNRN b - - 0 1"
    # stockfish.set_fen_position(fen1)
    # print(stockfish.get_board_visual())
    # piece_to_move, move, removed_piece, message = play_turn(fen1)
    # print(move)
    # stockfish.set_fen_position(create_fen_from_list_pieces())
    # print(stockfish.get_board_visual())

    delta_sum = 0
    log_game = False

    for i in range(0, 100):
        start = datetime.datetime.now()

        print("Game " + str(i))

        list_move = play_solo()
        print('\n' + str(list_move))
        print("Game duration : " + str(datetime.datetime.now() - start))

        delta = datetime.datetime.now() - start
        delta_sum += delta.total_seconds()
        print("Time : " + str(delta.total_seconds()) + "s")
        mean_delta = delta_sum / (i + 1)
        print("Mean time : " + str(mean_delta) + "s")

# endregion test
