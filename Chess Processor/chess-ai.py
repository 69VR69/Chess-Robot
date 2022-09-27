from stockfish import Stockfish


def compare(fen1, fen2):
    moveplayed = ""

    lines1 = fen1.split(" ")[0].split("/", 8)
    lines2 = fen2.split(" ")[0].split("/", 8)

    print(fen1)
    print(lines1)
    print(fen2)
    print(lines2)

    for i in range(len(lines1)):
        if lines1[i] == lines2[i]:
            continue
        else:
            print("line " + str(9 - i))
            print(lines1[i] + " != " + lines2[i])

    return moveplayed


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

    fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen2 = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"
    print(compare(fen1, fen2))
