from sudoku import Sudoku
from hillClimbing import HillClimbingSolver
from astar import astar_solver
import time

def main():
    print("Bienvenue dans le solveur de Sudoku !\n")
    difficulty = input("Choisissez la grille (easy / medium / hard / expert) : ").strip()
    algo = input("Choisissez l'algorithme (hill / astar) : ").strip()

    sudoku = Sudoku.from_file(f'grids/{difficulty}.txt')
    print("\nGrille initiale :")
    sudoku.display()

    if algo == "hill":
        #chrono commence !!!
        start_time = time.time()
        solver = HillClimbingSolver(sudoku)
        solution, iterations, conflicts = solver.solve()
        #chrono finit !!!
        end_time = time.time()
        elapsed_time = end_time - start_time
        if solution:
            print(f"\nRésolu en {iterations} itérations, {conflicts} conflits restants, en {elapsed_time:.2f} secondes.")
        else:
            print("\nÉchec de la résolution.")
        
        print(f"\nRésolu en {iterations} itérations, {conflicts} conflits restants.")
    elif algo == "astar":
        #chrono commence !!!
        start_time = time.time()
        solution, iterations = astar_solver(sudoku)
        #chrono finit !!!
        end_time = time.time()
        elapsed_time = end_time - start_time
        if solution:
            print(f"\nRésolu en {iterations} itérations, en {elapsed_time:.2f} secondes.")
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