# Fifteen Puzzle Solver (SISE Project)

This project was developed as part of the **Artificial Intelligence and Expert Systems** course. It implements a solver for the classic **Fifteen Puzzle** using various state-space search strategies.

## Task Overview

The Fifteen Puzzle consists of a 4x4 board with 15 numbered tiles and one empty space. The goal is to move the tiles by sliding them into the empty space to achieve the target configuration:
```
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 0
```

The program supports solving puzzles of **any size** (including non-square layouts), not just the standard 4x4.

## Implemented Algorithms

- **Breadth-First Search (BFS)**
- **Depth-First Search (DFS)** – with recursion depth limit
- **A\*** with the following heuristics:
  - **Hamming distance**
  - **Manhattan distance**

Each algorithm finds a valid sequence of moves (`L`, `R`, `U`, `D`) that solves the puzzle, if a solution exists.

## Input and Output

### Input file format

A text file with:
- The first line: two integers `rows` and `columns`.
- The next `rows` lines: space-separated integers representing the puzzle grid (0 represents the empty tile).

Example:
```
4 4
1 2 7 0
8 9 12 10
13 3 6 4
15 14 11 5
```

### Output solution file

Two lines:
1. Length of the solution (or `-1` if no solution found)
2. Sequence of moves (`L`, `R`, `U`, `D`)

### Output stats file

Five lines:
1. Length of the solution (or `-1`)
2. Number of visited states
3. Number of processed states
4. Maximum depth reached
5. Execution time in seconds (to 3 decimal places)

## Usage

The program is executed with the following command-line format:
```
program <strategy> <parameter> <input_file> <solution_file> <stats_file>
```

### Parameters

| Strategy | Argument | Parameter                  |
|----------|----------|----------------------------|
| `bfs`    | BFS      | Move order (e.g. `RDUL`)   |
| `dfs`    | DFS      | Move order (e.g. `LUDR`)   |
| `astr`   | A*       | Heuristic: `hamm` or `manh`|

### Example usages:
```
program bfs RDUL input.txt solution.txt stats.txt
program dfs LUDR input.txt solution.txt stats.txt
program astr manh input.txt solution.txt stats.txt
```

## Batch Execution Scripts

To simplify testing and benchmarking, this repository includes batch scripts:

- `run_all.sh` – Bash script for Linux/macOS
- `run_all.ps1` – PowerShell script for Windows

These scripts run the solver on multiple test files and store both solution and statistics output automatically.

## Research Component

This project also includes a research component that compares the performance of all search strategies on 413 puzzle instances with distances from 1 to 7 moves from the goal state. The results were visualized using bar charts and used for comparative analysis.

---
