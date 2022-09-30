from stockfish import Stockfish

stockfish = Stockfish('stockfish_15_win_x64_popcnt/stockfish_15_win_x64_popcnt/stockfish_15_x64_popcnt.exe')


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


def is_legal_move(fen, move):
    if len(move) != 4:
        print("Invalid move : not enough characters")
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
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    return stockfish.get_best_move()


def play_solo():
    return {}


if __name__ == '__main__':
    print('')

    stockfish.set_elo_rating(2000)

    fen1 = "qbrkbnrn/pppppppp/8/8/8/8/PPPPPPPP/QBRKBNRN w - - 0 1"
    fen2 = "qbrkbnrn/pppppppp/8/8/8/3P4/PPP1PPPP/QBRKBNRN b - - 0 1"
    stockfish.set_fen_position(fen1)
    print(stockfish.get_board_visual())
    move = compare(fen1, fen2)
    print('is ' + move + ' a legal move : ' + str(is_legal_move(fen1, move)))
    print('is the game over : ' + str(is_game_over()))
