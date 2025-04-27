import random
import copy

def count_conflicts(grid):
    conflicts = 0
    # lignes
    for row in grid:
        conflicts += 9 - len(set(row))
    # colonnes
    for col in zip(*grid):
        conflicts += 9 - len(set(col))
    # blocs 3x3
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(grid[box_row+i][box_col+j])
            conflicts += 9 - len(set(block))
    return conflicts

def hill_climbing_solver(sudoku, max_iterations=10000):
    grid = copy.deepcopy(sudoku.grid)

    # Remplir aléatoirement les cases vides dans chaque bloc 3x3
    for box_row in range(0,9,3):
        for box_col in range(0,9,3):
            nums = set(range(1,10))
            for i in range(3):
                for j in range(3):
                    if grid[box_row+i][box_col+j] != 0:
                        nums.discard(grid[box_row+i][box_col+j])
            nums = list(nums)
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    if grid[box_row+i][box_col+j] == 0:
                        grid[box_row+i][box_col+j] = nums.pop()

    current_conflicts = count_conflicts(grid)
    iterations = 0

    while current_conflicts > 0 and iterations < max_iterations:
        # Choisir un bloc 3x3 aléatoirement
        box_row, box_col = random.choice([0,3,6]), random.choice([0,3,6])

        # Trouver deux cases libres à échanger dans le bloc
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if sudoku.grid[box_row+i][box_col+j] == 0:
                    empty_cells.append((box_row+i, box_col+j))
        
        if len(empty_cells) >= 2:
            a, b = random.sample(empty_cells, 2)

            # Essayer d'échanger
            grid[a[0]][a[1]], grid[b[0]][b[1]] = grid[b[0]][b[1]], grid[a[0]][a[1]]
            new_conflicts = count_conflicts(grid)

            # Garder le changement si amélioration
            if new_conflicts < current_conflicts:
                current_conflicts = new_conflicts
            else:
                # Sinon revenir en arrière
                grid[a[0]][a[1]], grid[b[0]][b[1]] = grid[b[0]][b[1]], grid[a[0]][a[1]]

        iterations += 1

    return grid, iterations, current_conflicts
