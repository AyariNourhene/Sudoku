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
