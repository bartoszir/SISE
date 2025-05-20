LAST_COL_INDEX = None
LAST_ROW_INDEX = None

FINAL_STATE_BOARD = [
    [ '1', '2', '3', '4'],
    [ '5', '6', '7', '8'],
    [ '9','10','11','12'],
    ['13','14','15', '0'],
]

def clone_board(board):
    copied_board = []
    for row in board:
        copied_board.append(row.copy())
    return copied_board

''' file format
4 4
1 2 3 4
5 6 7 8
9 10 11 0
13 14 15 12
'''
def read_board_from_file(filename):
    global LAST_COL_INDEX, LAST_ROW_INDEX

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line for line in f.read().split('\n')]
        rows, cols = map(int, lines[0].split()) # pierwszy wiersz informuje o rozmiarze wiersza i kolumny
        board = []
        for line in lines[1:]:
            if line.strip():
                board.append(list(map(str, line.split())))
        LAST_ROW_INDEX = rows - 1
        LAST_COL_INDEX = cols - 1

        return board, rows, cols

def find_empty_field(board, rows, cols):
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '0':
                return i, j

def is_move_available(move, empty_field_coordinates):
    r, c = empty_field_coordinates
    if move == 'L':
        if c > 0:
            return True
    elif move == 'R':
        if c < LAST_COL_INDEX:
            return True
    elif move == 'U':
        if r > 0:
            return True
    elif move == 'D':
        if r < LAST_ROW_INDEX:
            return True
    else:
        return False

def is_goal(test_board, final_board):
    return test_board == final_board

def save_to_output_files(results, solution_filename, stats_filename):
    # najpierw plik z rozwiazaniem
    with open(solution_filename, 'w', encoding='utf-8') as f:
        if results["solution"] is None:
            f.write("-1\n")
        else:
            f.write(str(len(results["solution"])) + "\n")
            f.write("".join(results["solution"]))

    # plik z dodatkowymi informacjami
    with open(stats_filename, 'w', encoding='utf-8') as f:
        if results["solution"] is None:
            f.write("-1\n")
        else:
            f.write(str(len(results["solution"])) + "\n")
        f.write(str(results["visited"]) + "\n")
        f.write(str(results["processed"]) + "\n")
        f.write(str(results["max_depth"]) + "\n")
        f.write(str(results["time"]))