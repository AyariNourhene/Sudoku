import pygame
import time
from sudoku import Sudoku
from hillClimbing import HillClimbingSolver
from astar import astar_solver

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 600, 780
GRID_SIZE = 540  # Taille de la grille Sudoku (9x9)
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solveur de Sudoku")

# Polices
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)
BUTTON_FONT = pygame.font.Font(None, 28)

# Classe Sudoku GUI
class SudokuGUI:
    def __init__(self):
        self.sudoku = None
        self.solution = None
        self.selected_cell = None  # Pour suivre la cellule sélectionnée
        self.cell_size = GRID_SIZE // 9  # Taille de chaque cellule du Sudoku
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = "easy"  # Difficulté par défaut
        self.algorithm = "hill"  # Algorithme par défaut
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Variables pour les résultats
        self.iterations = 0
        self.conflicts = 0
        self.execution_time = 0.0
        self.solved = False
        self.error_message = ""

        # Position de la grille
        self.grid_x = (WIDTH - GRID_SIZE) // 2
        self.grid_y = 150

        # Boutons
        self.create_buttons()

    def create_buttons(self):
        button_width = 100
        button_height = 40
        spacing = 20
        
        # Boutons de difficulté
        self.difficulty_buttons = {
            "easy": pygame.Rect(50, 50, button_width, button_height),
            "medium": pygame.Rect(50 + button_width + spacing, 50, button_width, button_height),
            "hard": pygame.Rect(50 + 2*(button_width + spacing), 50, button_width, button_height)
        }

        # Boutons d'algorithme
        self.algorithm_buttons = {
            "hill": pygame.Rect(50, 100, button_width, button_height),
            "astar": pygame.Rect(50 + button_width + spacing, 100, button_width, button_height)
        }

        # Bouton Résoudre
        self.solve_button = pygame.Rect(WIDTH - 150, 100, button_width, button_height)
        
        # Bouton Réinitialiser
        self.reset_button = pygame.Rect(WIDTH - 150, 50, button_width, button_height)

    def display_grid(self):
        window.fill(WHITE)

        # Dessiner la grille 9x9
        for i in range(10):
            # Lignes verticales
            pygame.draw.line(
                window, 
                BLACK, 
                (self.grid_x + i * self.cell_size, self.grid_y), 
                (self.grid_x + i * self.cell_size, self.grid_y + GRID_SIZE), 
                3 if i % 3 == 0 else 1
            )
            # Lignes horizontales
            pygame.draw.line(
                window, 
                BLACK, 
                (self.grid_x, self.grid_y + i * self.cell_size), 
                (self.grid_x + GRID_SIZE, self.grid_y + i * self.cell_size), 
                3 if i % 3 == 0 else 1
            )

        # Dessiner les numéros dans la grille
        for row in range(9):
            for col in range(9):
                number = self.grid[row][col]
                if number != 0:
                    color = BLUE
                    if self.selected_cell == (row, col):
                        color = RED
                    elif self.solution and self.solution[row][col] != self.grid[row][col]:
                        color = GREEN  # Nombres ajoutés par la solution
                    
                    num_text = FONT.render(str(number), True, color)
                    window.blit(
                        num_text, 
                        (self.grid_x + col * self.cell_size + self.cell_size // 3, 
                         self.grid_y + row * self.cell_size + self.cell_size // 4)
                    )

        # Dessiner les boutons
        self.draw_buttons()
        
        # Afficher les résultats
        self.display_results()
        
        # Afficher les messages d'erreur
        if self.error_message:
            error_text = SMALL_FONT.render(self.error_message, True, RED)
            window.blit(error_text, (10, HEIGHT - 90))

        pygame.display.flip()

    def display_results(self):
        if self.solved:
            status_text = SMALL_FONT.render("Status: Solved!", True, GREEN)
        else:
            status_text = SMALL_FONT.render("Status: Unsolved", True, RED)
        
        window.blit(status_text, (10, HEIGHT - 80))
        window.blit(SMALL_FONT.render(f"Iterations: {self.iterations}", True, BLACK), (10, HEIGHT - 60))
        window.blit(SMALL_FONT.render(f"Conflicts: {self.conflicts}", True, BLACK), (10, HEIGHT - 40))
        window.blit(SMALL_FONT.render(f"Time: {self.execution_time:.3f} sec", True, BLACK), (10, HEIGHT - 20))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Vérifier les clics sur les boutons
                for name, rect in self.difficulty_buttons.items():
                    if rect.collidepoint(x, y):
                        self.difficulty = name
                        self.reset_grid()
                
                for name, rect in self.algorithm_buttons.items():
                    if rect.collidepoint(x, y):
                        self.algorithm = name
                
                if self.solve_button.collidepoint(x, y):
                    self.solve()
                
                if self.reset_button.collidepoint(x, y):
                    self.reset_grid()
                
                # Vérifier les clics sur la grille
                if (self.grid_x <= x <= self.grid_x + GRID_SIZE and 
                    self.grid_y <= y <= self.grid_y + GRID_SIZE):
                    col = (x - self.grid_x) // self.cell_size
                    row = (y - self.grid_y) // self.cell_size
                    self.selected_cell = (row, col)
                else:
                    self.selected_cell = None
            
            elif event.type == pygame.KEYDOWN and self.selected_cell:
                row, col = self.selected_cell
                if event.key == pygame.K_1: self.grid[row][col] = 1
                elif event.key == pygame.K_2: self.grid[row][col] = 2
                elif event.key == pygame.K_3: self.grid[row][col] = 3
                elif event.key == pygame.K_4: self.grid[row][col] = 4
                elif event.key == pygame.K_5: self.grid[row][col] = 5
                elif event.key == pygame.K_6: self.grid[row][col] = 6
                elif event.key == pygame.K_7: self.grid[row][col] = 7
                elif event.key == pygame.K_8: self.grid[row][col] = 8
                elif event.key == pygame.K_9: self.grid[row][col] = 9
                elif event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE: 
                    self.grid[row][col] = 0
                self.solved = False

    def draw_buttons(self):
        # Dessiner les boutons de difficulté
        for name, rect in self.difficulty_buttons.items():
            color = GREEN if self.difficulty == name else BLUE
            pygame.draw.rect(window, color, rect)
            text = BUTTON_FONT.render(name.capitalize(), True, WHITE)
            window.blit(text, (rect.x + 10, rect.y + 10))
        
        # Dessiner les boutons d'algorithme
        for name, rect in self.algorithm_buttons.items():
            color = GREEN if self.algorithm == name else BLUE
            pygame.draw.rect(window, color, rect)
            text = BUTTON_FONT.render("Hill" if name == "hill" else "A*", True, WHITE)
            window.blit(text, (rect.x + 10, rect.y + 10))
        
        # Bouton Résoudre
        pygame.draw.rect(window, BLUE, self.solve_button)
        text = BUTTON_FONT.render("Solve", True, WHITE)
        window.blit(text, (self.solve_button.x + 10, self.solve_button.y + 10))
        
        # Bouton Réinitialiser
        pygame.draw.rect(window, RED, self.reset_button)
        text = BUTTON_FONT.render("Reset", True, WHITE)
        window.blit(text, (self.reset_button.x + 10, self.reset_button.y + 10))

    def reset_grid(self):
        try:
            self.sudoku = Sudoku.from_file(f'grids/{self.difficulty}.txt')
            self.grid = [row[:] for row in self.sudoku.grid]
            self.solution = None
            self.solved = False
            self.iterations = 0
            self.conflicts = 0
            self.execution_time = 0.0
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error loading {self.difficulty} grid: {str(e)}"
            self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def solve(self):
        try:
            # Créer un objet Sudoku à partir de la grille actuelle
            self.sudoku = Sudoku(self.grid)
            
            start_time = time.time()
            
            if self.algorithm == "hill":
                solver = HillClimbingSolver(self.sudoku)
                self.solution, self.iterations, self.conflicts = solver.solve()
            elif self.algorithm == "astar":
                self.solution, self.iterations = astar_solver(self.sudoku)
                self.conflicts = 0
            
            self.execution_time = time.time() - start_time
            
            if self.solution:
                self.solved = True
                # Mettre à jour la grille avec la solution
                for i in range(9):
                    for j in range(9):
                        if self.grid[i][j] == 0:  # Ne remplacer que les cases vides
                            self.grid[i][j] = self.solution[i][j]
            else:
                self.error_message = "No solution found!"
                
        except Exception as e:
            self.error_message = f"Solving error: {str(e)}"

# Boucle principale du jeu
def main():
    sudoku_gui = SudokuGUI()
    sudoku_gui.reset_grid()  # Charger une grille initiale

    while sudoku_gui.running:
        sudoku_gui.handle_input()
        sudoku_gui.display_grid()
        sudoku_gui.clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()