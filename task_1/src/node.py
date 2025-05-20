from dataclasses import dataclass

# from my modules
from utils import clone_board

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

def get_node_path(node: Node):
    path = []
    while node.parent is not None:
        path.append(node.last_move)
        node = node.parent
    return path[::-1] # zwracamy te liste w odwrotnej kolejnosci