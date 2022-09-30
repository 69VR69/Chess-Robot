from stockfish import Stockfish
from chessnut import Chessnut


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
                        move_played += str(chr(65 + j)) + str(8 - i)
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


def is_legal_move(fen, move):
    result = False

    if len(move) != 4:
        return result

    if (move[0] < 'A' or move[0] > 'H') or (move[2] < 'A' or move[2] > 'H'):
        if(move[1] < '1' or move[1] > '8') or (move[3] < '1' or move[3] > '8'):
            return result

    chessnut = Chessnut()
    chessnut.set_fen(fen)
    result = chessnut.is_legal(move)

    return result

def detect_end_of_game(fen):
    return {}


def find_next_move(fen):
    stockfish = Stockfish('stockfish_15_win_x64_popcnt/stockfish_15_win_x64_popcnt/stockfish_15_x64_popcnt.exe')
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    return stockfish.get_best_move()


def play_solo():
    return {}


if __name__ == '__main__':
    print("")

    fen1 = "qbrkbnrn/pppppppp/8/8/8/8/PPPPPPPP/QBRKBNRN w - - 0 1"
    fen2 = "qbrkbnrn/pppppppp/8/8/8/3P4/PPP1PPPP/QBRKBNRN b - - 0 1"
    fen3 = "qbrkbnrn/ppppp1pp/5p2/8/8/3P4/PPP1PPPP/QBRKBNRN w - - 0 1"
    move1 = compare(fen1, fen2)
    print(move1)
    print(is_legal_move(fen1, move1))
    #print(compare(fen2, fen3))