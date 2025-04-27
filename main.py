from sudoku import Sudoku
from hillClimbing import HillClimbingSolver
from astar import astar_solver

def main():
    print("Bienvenue dans le solveur de Sudoku !\n")
    difficulty = input("Choisissez la grille (easy / medium / hard) : ").strip()
    algo = input("Choisissez l'algorithme (hill / astar) : ").strip()

    sudoku = Sudoku.from_file(f'grids/{difficulty}.txt')
    print("\nGrille initiale :")
    sudoku.display()

    if algo == "hill":
        solver = HillClimbingSolver(sudoku)
        solution, iterations, conflicts = solver.solve()
        print(f"\nRésolu en {iterations} itérations, {conflicts} conflits restants.")
    elif algo == "astar":
        solution, iterations = astar_solver(sudoku)
        if solution:
            print(f"\nRésolu en {iterations} itérations.")
        else:
            print("\nÉchec de la résolution.")
    else:
        print("Algorithme inconnu.")
        return

    if solution:
        solved_sudoku = Sudoku(solution)
        print("\nGrille finale :")
        solved_sudoku.display()

if __name__ == "__main__":
    main()