import random
import copy
from typing import List, Tuple, Optional

class HillClimbingSolver:
    def __init__(self, sudoku):
        self.original_grid = copy.deepcopy(sudoku.grid)
        self.current_grid = None
        self.best_solution = None
        self.best_conflicts = float('inf')

    def count_conflicts(self, grid):
        """Calcule le nombre total de conflits"""
        conflicts = 0
        # Vérification des lignes
        for row in grid:
            conflicts += 9 - len(set(row))
        # Vérification des colonnes
        for col in zip(*grid):
            conflicts += 9 - len(set(col))
        # Vérification des blocs 3x3
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                block = [grid[box_row+i][box_col+j] for i in range(3) for j in range(3)]
                conflicts += 9 - len(set(block))
        return conflicts

    def heuristic(self, grid):
        """Heuristique combinant cases vides et conflits"""
        empty_cells = sum(row.count(0) for row in grid)
        return empty_cells + self.count_conflicts(grid)

    def initialize_grid(self):
        """Initialise une grille aléatoire valide par bloc"""
        grid = copy.deepcopy(self.original_grid)
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                nums = set(range(1,10)) - {grid[box_row+i][box_col+j] 
                                         for i in range(3) for j in range(3) 
                                         if grid[box_row+i][box_col+j] != 0}
                nums = list(nums)
                random.shuffle(nums)
                for i in range(3):
                    for j in range(3):
                        if grid[box_row+i][box_col+j] == 0:
                            grid[box_row+i][box_col+j] = nums.pop()
        return grid

    def get_neighbor(self, grid):
        """Génère un voisin en échangeant 2 cases modifiables"""
        new_grid = copy.deepcopy(grid)
        while True:
            box_row, box_col = random.choice([0,3,6]), random.choice([0,3,6])
            modifiable = [(i,j) for i in range(box_row, box_row+3) 
                            for j in range(box_col, box_col+3) 
                            if self.original_grid[i][j] == 0]
            if len(modifiable) >= 2:
                a, b = random.sample(modifiable, 2)
                new_grid[a[0]][a[1]], new_grid[b[0]][b[1]] = new_grid[b[0]][b[1]], new_grid[a[0]][a[1]]
                return new_grid

    def solve(self, max_iterations=10000, max_restarts=5):
        """Algorithme principal avec redémarrages"""
        total_iterations = 0
        for restart in range(max_restarts):
            current_grid = self.initialize_grid()
            current_heuristic = self.heuristic(current_grid)
            
            for iteration in range(max_iterations):
                neighbor = self.get_neighbor(current_grid)
                neighbor_heuristic = self.heuristic(neighbor)
                total_iterations += 1
                
                if neighbor_heuristic < current_heuristic:
                    current_grid = neighbor
                    current_heuristic = neighbor_heuristic
                    
                    current_conflicts = self.count_conflicts(current_grid)
                    if current_conflicts < self.best_conflicts:
                        self.best_solution = copy.deepcopy(current_grid)
                        self.best_conflicts = current_conflicts
                        if current_conflicts == 0:
                            return self.best_solution, total_iterations, self.best_conflicts
        
        return self.best_solution, total_iterations, self.best_conflicts