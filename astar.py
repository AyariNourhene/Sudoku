import heapq
import copy

class Node:
    def __init__(self, grid, cost, heuristic):
        self.grid = grid
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def is_valid(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row//3), 3 * (col//3)
    for i in range(3):
        for j in range(3):
            if grid[start_row+i][start_col+j] == num:
                return False
    return True

def heuristic(grid):
    return sum(row.count(0) for row in grid)

def astar_solver(sudoku):
    start_grid = copy.deepcopy(sudoku.grid)
    open_list = []
    heapq.heappush(open_list, Node(start_grid, 0, heuristic(start_grid)))
    iterations = 0

    while open_list:
        current_node = heapq.heappop(open_list)
        current_grid = current_node.grid

        empty = find_empty(current_grid)
        if not empty:
            return current_grid, iterations

        row, col = empty

        for num in range(1, 10):
            if is_valid(current_grid, row, col, num):
                new_grid = copy.deepcopy(current_grid)
                new_grid[row][col] = num
                heapq.heappush(open_list, Node(new_grid, current_node.cost + 1, heuristic(new_grid)))

        iterations += 1

    return None, iterations
