import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sudoku import Sudoku
from hillClimbing import hill_climbing_solver
from astar import astar_solver

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solveur de Sudoku")
        self.root.geometry("700x600")
        
        self.sudoku = None
        self.solution = None
        self.create_widgets()
        
    def create_widgets(self):
        # Frame pour les contrôles
        control_frame = ttk.LabelFrame(self.root, text="Contrôles", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Sélection de difficulté
        ttk.Label(control_frame, text="Difficulté:").grid(row=0, column=0, sticky=tk.W)
        self.difficulty = ttk.Combobox(control_frame, values=["easy", "medium", "hard"])
        self.difficulty.grid(row=0, column=1, sticky=tk.W)
        self.difficulty.set("easy")
        
        # Sélection d'algorithme
        ttk.Label(control_frame, text="Algorithme:").grid(row=1, column=0, sticky=tk.W)
        self.algorithm = ttk.Combobox(control_frame, values=["hill", "astar"])
        self.algorithm.grid(row=1, column=1, sticky=tk.W)
        self.algorithm.set("hill")
        
        # Boutons
        ttk.Button(control_frame, text="Charger", command=self.load_grid).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Résoudre", command=self.solve).grid(row=1, column=2, padx=5)
        ttk.Button(control_frame, text="Réinitialiser", command=self.reset).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Quitter", command=self.root.quit).grid(row=1, column=3, padx=5)
        
        # Frame pour la grille
        self.grid_frame = ttk.LabelFrame(self.root, text="Grille de Sudoku", padding=10)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame pour les résultats
        self.result_frame = ttk.LabelFrame(self.root, text="Résultats", padding=10)
        self.result_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.result_frame, text="Itérations:").grid(row=0, column=0, sticky=tk.W)
        self.iterations_label = ttk.Label(self.result_frame, text="0")
        self.iterations_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.result_frame, text="Conflits:").grid(row=1, column=0, sticky=tk.W)
        self.conflicts_label = ttk.Label(self.result_frame, text="0")
        self.conflicts_label.grid(row=1, column=1, sticky=tk.W)
        
        # Initialiser la grille vide
        self.init_grid()
        
    def init_grid(self):
        # Créer les cellules de la grille
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = ttk.Entry(self.grid_frame, width=3, font=('Arial', 16), justify='center')
                cell.grid(row=i, column=j, padx=1, pady=1, ipady=5)
                
                # Ajouter des bordures pour les blocs 3x3
                if i % 3 == 0 and i != 0:
                    cell.grid(pady=(3,1))
                if j % 3 == 0 and j != 0:
                    cell.grid(padx=(3,1))
                
                row.append(cell)
            self.cells.append(row)
    
    def load_grid(self):
        try:
            difficulty = self.difficulty.get()
            self.sudoku = Sudoku.from_file(f'grids/{difficulty}.txt')
            self.display_grid(self.sudoku.grid)
            self.clear_results()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger la grille: {e}")
    
    def display_grid(self, grid):
        for i in range(9):
            for j in range(9):
                value = grid[i][j] if grid[i][j] != 0 else ""
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].insert(0, str(value))
                
                # Mettre en évidence les cellules fixes (non vides initialement)
                if grid[i][j] != 0:
                    self.cells[i][j].config(state='readonly', foreground='blue')
                else:
                    self.cells[i][j].config(state='normal', foreground='black')
    
    def solve(self):
        if not self.sudoku:
            messagebox.showwarning("Attention", "Veuillez d'abord charger une grille")
            return
            
        algo = self.algorithm.get()
        
        if algo == "hill":
            solution, iterations, conflicts = hill_climbing_solver(self.sudoku)
            self.solution = solution
            self.iterations_label.config(text=str(iterations))
            self.conflicts_label.config(text=str(conflicts))
        elif algo == "astar":
            solution, iterations = astar_solver(self.sudoku)
            self.solution = solution
            self.iterations_label.config(text=str(iterations))
            self.conflicts_label.config(text="0")  # A* trouve toujours une solution sans conflits
            
        if solution:
            self.display_grid(solution)
        else:
            messagebox.showinfo("Information", "La résolution a échoué")
    
    def reset(self):
        if self.sudoku:
            self.display_grid(self.sudoku.grid)
            self.clear_results()
    
    def clear_results(self):
        self.iterations_label.config(text="0")
        self.conflicts_label.config(text="0")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

