import sys

# from my modules
from node import Node, CurrentState
from utils import read_board_from_file, find_empty_field, save_to_output_files
from algorithms import dfs, bfs, astr


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