from stockfish import Stockfish


def compare(fen1, fen2):
    move_played = ""

    lines1 = fen1.split(" ")[0].split("/", 8)
    lines2 = fen2.split(" ")[0].split("/", 8)

    for i in reversed(range(len(lines1))):
        if lines1[i] == lines2[i]:
            continue
        else:
            # print("line1: " + lines1[i])
            # print("line2: " + lines2[i])
            temp1 = stringify_fen(lines1[i])
            temp2 = stringify_fen(lines2[i])
            for j in range(len(temp1)):
                if temp1[j] == temp2[j]:
                    continue
                else:
                    print("move: (" + str(chr(65 + j)) + "," + str(8-i)+")")
                    if temp1[j] != "." or temp2[j] != ".":
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


def detect_not_legal_move(fen):
    return {}


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
    print(compare(fen1, fen2))
    print(compare(fen2, fen3))
    print(compare(fen1, fen3))
