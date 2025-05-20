from collections import deque
from dataclasses import dataclass
from time import time
import heapq
import sys

# ---------------------------------------------------------------------
# Global variables

FINAL_STATE_BOARD = [
    [ '1', '2', '3', '4'],
    [ '5', '6', '7', '8'],
    [ '9','10','11','12'],
    ['13','14','15', '0'],
]

LAST_COL_INDEX = None
LAST_ROW_INDEX = None

# ---------------------------------------------------------------------

@dataclass
class CurrentState:
    board: list
    empty_field: (int, int) # (row, col)


class Node:
    def __init__(self, state: CurrentState, parent=None, last_move=None):
        self.state = state
        self.parent = parent
        self.last_move = last_move
        self.depth = parent.depth + 1 if parent else 0


    def create_child(self, child_state: CurrentState, move: str):
        return Node(state=child_state, parent=self, last_move=move)

    def make_move(self, move):
        empty_field = self.state.empty_field
        copied_board = clone_board(self.state.board)


        r, c = empty_field
        if move == 'L':
            tmp = copied_board[r][c]
            copied_board[r][c] = copied_board[r][c - 1]
            copied_board[r][c - 1] = tmp
            new_state = CurrentState(
                board=copied_board,
                empty_field=(r, c - 1)
            )
            return self.create_child(child_state=new_state, move=move)

        elif move == 'R':
            tmp = copied_board[r][c]
            copied_board[r][c] = copied_board[r][c + 1]
            copied_board[r][c + 1] = tmp
            new_state = CurrentState(
                board=copied_board,
                empty_field=(r, c + 1)
            )
            return self.create_child(child_state=new_state, move=move)

        elif move == 'U':
            tmp = copied_board[r][c]
            copied_board[r][c] = copied_board[r - 1][c]
            copied_board[r - 1][c] = tmp
            new_state = CurrentState(
                board=copied_board,
                empty_field=(r - 1, c)
            )
            return self.create_child(child_state=new_state, move=move)

        elif move == 'D':
            tmp = copied_board[r][c]
            copied_board[r][c] = copied_board[r + 1][c]
            copied_board[r + 1][c] = tmp
            new_state = CurrentState(
                board=copied_board,
                empty_field=(r + 1, c)
            )
            return self.create_child(child_state=new_state, move=move)

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state.board))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.state.board == other.state.board

# ---------------------------------------------------------------------
# Utils

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

def get_node_path(node: Node):
    path = []
    while node.parent is not None:
        path.append(node.last_move)
        node = node.parent
    return path[::-1] # zwracamy te liste w odwrotnej kolejnosci

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

# ---------------------------------------------------------------------
# ALGORITHMS

def bfs(root_node: Node, move_order):
    start_time = time()

    if is_goal(root_node.state.board, FINAL_STATE_BOARD):
        return {
            "solution": get_node_path(root_node),
            "visited": 1,
            "processed": 0,
            "max_depth": 0,
            "time": round(time() - start_time, 3)
        }

    queue = deque()  # lista stanow otwartych
    visited = set()  # lista stanow odwiedzonych

    queue.append(root_node)
    visited.add(root_node)

    processed = 0
    max_depth = 0

    while queue:
        current_node = queue.popleft()
        processed += 1

        for move in move_order:
            try:
                if is_move_available(move=move, empty_field_coordinates=current_node.state.empty_field):
                    neighbour = current_node.make_move(move)

                    if neighbour not in visited:
                        if is_goal(neighbour.state.board, FINAL_STATE_BOARD):
                            return {
                                "solution": get_node_path(neighbour),
                                "visited": len(visited),
                                "processed": processed,
                                "max_depth": max_depth,
                                "time": round(time() - start_time, 5)
                                # "time": time() - start_time
                            }

                        visited.add(neighbour)
                        queue.append(neighbour)
                        max_depth = max(max_depth, neighbour.depth) # wyzej
            except Exception:
                continue # jesli ruchy wykraczaja poza plansze to je ignorujemy

    # return FAILURE
    return {
        "solution": None,
        "visited": len(visited),
        "processed": processed,
        "max_depth": max_depth,
        "time": round(time() - start_time, 5)
    }


def dfs(root_node: Node, move_order, max_depth_limit=20):
    start_time = time()

    if is_goal(root_node.state.board, FINAL_STATE_BOARD):
        return {
            "solution": get_node_path(root_node),
            "visited": 1,
            "processed": 0,
            "max_depth": 0,
            "time": round(time() - start_time, 5)
        }

    stack = list()  # lista stanow otwartych
    visited = set() # lista stanow zamknietych

    stack.append(root_node)

    processed = 0
    max_depth = 0

    while stack:
        current_node = stack.pop()
        processed += 1

        if current_node not in visited:
            visited.add(current_node)

            current_depth = current_node.depth
            max_depth = max(max_depth, current_depth)

            if current_depth >= max_depth_limit:
                continue

            for move in reversed(move_order):
                try:
                    if is_move_available(move=move, empty_field_coordinates=current_node.state.empty_field):
                        neighbour = current_node.make_move(move)

                        if neighbour not in visited:
                            if is_goal(neighbour.state.board, FINAL_STATE_BOARD):
                                return {
                                    "solution": get_node_path(neighbour),
                                    "visited": len(visited),
                                    "processed": processed,
                                    "max_depth": max(max_depth, neighbour.depth),
                                    "time": round(time() - start_time, 5)
                                }
                            stack.append(neighbour)
                except Exception:
                    continue
    # return FAILURE
    return {
        "solution": None,
        "visited": len(visited),
        "processed": processed,
        "max_depth": max_depth,
        "time": round(time() - start_time, 5)
    }

def astr(root_node: Node, heuristic_type='hamm'):
    start_time = time()

    priority_queue = list()
    visited = set()
    counter = 0  # do rozstrzygania w przypadku remisow wartosci f()

    # f(n) = g(n) + h(n)
    f = 0
    heapq.heappush(priority_queue, (f, counter, root_node))
    counter += 1

    processed = 0
    max_depth = 0

    while priority_queue:
        _, _, current_node = heapq.heappop(priority_queue)
        processed += 1

        # return SUCCESS
        if is_goal(current_node.state.board, FINAL_STATE_BOARD):
            return {
                "solution": get_node_path(current_node),
                "visited": len(visited),
                "processed": processed,
                "max_depth": max_depth,
                "time": round(time() - start_time, 5)
            }

        if current_node not in visited:
            visited.add(current_node)

            for move in 'LRUD':
                if is_move_available(move=move, empty_field_coordinates=current_node.state.empty_field):
                    neighbour = current_node.make_move(move)

                    if neighbour not in visited:
                        if heuristic_type == 'hamm':
                            f = neighbour.depth + hamming_metric(neighbour.state.board, FINAL_STATE_BOARD)
                        elif heuristic_type == 'manh':
                            f = neighbour.depth + manhattan_metric(neighbour.state.board, FINAL_STATE_BOARD)
                        heapq.heappush(priority_queue, (f, counter, neighbour))
                        counter += 1
                        max_depth = max(max_depth, neighbour.depth)

    # return FAILURE
    return {
        "solution": None,
        "visited": len(visited),
        "processed": processed,
        "max_depth": max_depth,
        "time": round(time() - start_time, 5)
    }

# ---------------------------------------------------------------------
# Heuristics

''' zlicza ile elementow nie jest na swoim miejscu (z pominieciem 0) '''
def hamming_metric(board, final_board):
    mismatch = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] != '0' and board[r][c] != final_board[r][c]:
                mismatch += 1
    return mismatch


''' sumuje odleglosci kazdego elementu od swojego miejsca docelowego (z pominieciem 0)'''
def manhattan_metric(board, final_board):
    positions = {}
    distance = 0

    for r in range(len(final_board)):
        for c in range(len(final_board[0])):
            value = final_board[r][c]
            positions[value] = (r, c)

    for r in range(len(board)):
        for c in range(len(board[0])):
            value = board[r][c]
            if value != '0':
                target_r, target_c = positions[value]
                # sumujemy wartosc bezwzgledna z roznicy wspolrzednych, liczymy po prostu odleglosc miedzy punktami
                distance += abs(target_r - r) + abs(target_c - c)

    return distance

# ======================================================================

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("składnia:  program <strategia> <parametr> <plik wejściowy> <plik rozwiązania> <plik dodatkowych informacji>")
        sys.exit(1)

    strategy = sys.argv[1]
    strategy_param = sys.argv[2]
    input_file = sys.argv[3]
    solution_file = sys.argv[4]
    stats_file = sys.argv[5]

    board, rows, cols = read_board_from_file(input_file)

    r, c = find_empty_field(board, rows, cols)
    start_board = CurrentState(
        board=board,
        empty_field=(r, c)
    )

    root = Node(state=start_board)

    result = None
    if strategy == 'bfs':
        result = bfs(root_node=root, move_order=strategy_param)
    elif strategy == 'dfs':
        result = dfs(root_node=root, move_order=strategy_param)
    elif strategy == 'astr':
        result = astr(root_node=root, heuristic_type=strategy_param)
    else:
        print("Nieznana strategia.")
        sys.exit(1)

    save_to_output_files(results=result, solution_filename=solution_file, stats_filename=stats_file)