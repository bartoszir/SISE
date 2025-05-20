from collections import deque
from time import time
import heapq

# from my modules
from utils import *
from node import *

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
            if is_move_available(move=move, empty_field_coordinates=current_node.state.empty_field):
                neighbour = current_node.make_move(move)
                max_depth = max(max_depth, neighbour.depth)

                if neighbour not in visited:
                    if is_goal(neighbour.state.board, FINAL_STATE_BOARD):
                        return {
                            "solution": get_node_path(neighbour),
                            "visited": len(visited),
                            "processed": processed,
                            "max_depth": max_depth,
                            "time": round(time() - start_time, 5)
                        }

                    visited.add(neighbour)
                    queue.append(neighbour)
            else:
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

    stack = [root_node]  # lista stanow otwartych
    closed = set() # lista stanow zamknietych
    # stack.append(root_node)
    processed = 0
    max_depth = 0

    while stack:
        current_node = stack.pop()

        if current_node in closed:
            continue

        closed.add(current_node)

        current_depth = current_node.depth
        max_depth = max(max_depth, current_depth)

        if current_depth >= max_depth_limit:
            continue

        processed += 1 # wezel jest przetwarzany

        for move in reversed(move_order):
            if is_move_available(move=move, empty_field_coordinates=current_node.state.empty_field):
                neighbour = current_node.make_move(move)

                if neighbour not in closed:
                    if is_goal(neighbour.state.board, FINAL_STATE_BOARD):
                        return {
                            "solution": get_node_path(neighbour),
                            "visited": len(closed) + 1,
                            "processed": processed,
                            "max_depth": max(max_depth, neighbour.depth),
                            "time": round(time() - start_time, 5)
                        }
                    stack.append(neighbour)
            else:
                continue
    # return FAILURE
    return {
        "solution": None,
        "visited": len(closed),
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

        if current_node in visited:
            continue

        visited.add(current_node)
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
