class Sudoku:
    def __init__(self, grid):
        self.grid = grid

    @classmethod
    def from_file(cls, filename):
        grid = []
        with open(filename, 'r') as f:
            for line in f:
                grid.append([int(n) for n in line.strip().split()])
        return cls(grid)

    def display(self):
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(num if num != 0 else ".", end=" ")
            print()
        print()

    def is_valid(self, row, col, num):
        if num in self.grid[row]:
            return False
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row//3), 3 * (col//3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row+i][start_col+j] == num:
                    return False
        return True

    def is_complete(self):
        return all(all(cell != 0 for cell in row) for row in self.grid)
'''
import requests
import random
import copy
from typing import List

class Sudoku:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.original = copy.deepcopy(grid)

    @classmethod
    def from_api(cls, difficulty: str = "easy") -> 'Sudoku':
        """Charge une grille depuis une API en ligne avec gestion robuste des erreurs"""
        try:
            # API 1: sugoku (plus fiable)
            try:
                url = f"https://sugoku.onrender.com/board?difficulty={difficulty}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return cls(data['board'])
            except Exception as api1_error:
                print(f"API sugoku failed, trying backup: {api1_error}")

            # API 2: dosuku (backup)
            try:
                url = "https://sudoku-api.vercel.app/api/dosuku"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    # Correction ici: accès correct au champ 'grids'
                    if 'newboard' in data and 'grids' in data['newboard']:
                        grid_data = data['newboard']['grids'][0]['value']
                        return cls(grid_data)
            except Exception as api2_error:
                print(f"API dosuku failed: {api2_error}")

        except Exception as e:
            print(f"Erreur lors du chargement depuis l'API: {e}")

        # Fallback: grille locale
        return cls(cls.get_local_grid(difficulty))

    @staticmethod
    def get_local_grid(difficulty: str = "easy") -> List[List[int]]:
        """Retourne une grille locale selon la difficulté"""
        grids = {
            "easy": [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ],
            "medium": [
                [0, 0, 0, 0, 0, 0, 6, 8, 0],
                [0, 0, 0, 0, 7, 3, 0, 0, 9],
                [3, 0, 9, 0, 0, 0, 0, 4, 5],
                [4, 9, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 3, 0, 5, 0, 9, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 3, 6],
                [9, 6, 0, 0, 0, 0, 3, 0, 8],
                [7, 0, 0, 6, 8, 0, 0, 0, 0],
                [0, 2, 8, 0, 0, 0, 0, 0, 0]
            ],
            "hard": [
                [8, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 6, 0, 0, 0, 0, 0],
                [0, 7, 0, 0, 9, 0, 2, 0, 0],
                [0, 5, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 4, 5, 7, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 3, 0],
                [0, 0, 1, 0, 0, 0, 0, 6, 8],
                [0, 0, 8, 5, 0, 0, 0, 1, 0],
                [0, 9, 0, 0, 0, 0, 4, 0, 0]
            ]
        }
        return copy.deepcopy(grids.get(difficulty, grids["easy"]))

    def display(self):
        """Affiche la grille dans la console"""
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            print(" ".join(str(num) if num != 0 else "." for num in row))'''