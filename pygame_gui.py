import pygame
import time
from sudoku import Sudoku
from hillClimbing import HillClimbingSolver
from astar import astar_solver
import sys


pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN1 = (10, 30, 20)


WIDTH, HEIGHT = 600, 740
GRID_SIZE = 540  
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solveur de Sudoku")

FONT = pygame.font.Font(None, 36)
FONT2 = pygame.font.SysFont("comicsansms", 30)
SMALL_FONT = pygame.font.Font(None, 20)
SMALL_FONT1 = pygame.font.SysFont("comicsansms", 26)
BUTTON_FONT = pygame.font.Font(None, 28)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 60)

def show_welcome_screen():
    
    BACKGROUND_TOP = (30, 60, 50)
    BACKGROUND_BOTTOM = (10, 30, 20)
    TITLE_COLOR = (240, 255, 240)  
    BUTTON_COLOR = (40, 120, 80)
    HOVER_COLOR = (60, 180, 120)
    TEXT_COLOR = (240, 255, 240)
    SHADOW_COLOR = (10, 20, 10, 120)  
    COPYRIGHT_COLOR = (220, 220, 220)  

    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    def draw_vertical_gradient(surface, top_color, bottom_color):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            color = [
                int(top_color[i] * (1 - ratio) + bottom_color[i] * ratio)
                for i in range(3)
            ]
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))

    while True:
        # Gradient background
        draw_vertical_gradient(screen, BACKGROUND_TOP, BACKGROUND_BOTTOM)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or (
                event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(pygame.mouse.get_pos())
            ):
                return

        # Fonts
        title_font = pygame.font.SysFont("comicsansms", 80)
        title_font1 = pygame.font.SysFont("comicsansms", 70)

        title_text = title_font1.render("Welcome to", True, TITLE_COLOR)
        shadow_text = title_font1.render("Welcome to", True, (10, 20, 10))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        title_text2 = title_font.render("Sudoku Solver", True, TITLE_COLOR)
        shadow_text2 = title_font.render("Sudoku Solver", True, (10, 20, 10))
        title_rect2 = title_text2.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 90))

        screen.blit(shadow_text, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title_text, title_rect)
        screen.blit(shadow_text2, (title_rect2.x + 3, title_rect2.y + 3))
        screen.blit(title_text2, title_rect2)

        start_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 50, 220, 55)

        try:
            button_font = pygame.font.Font("fonts/roboto_medium.ttf", 30)
        except:
            button_font = pygame.font.SysFont("arial", 30, bold=True)

        button_hover = start_button.collidepoint(pygame.mouse.get_pos())
        button_color = HOVER_COLOR if button_hover else BUTTON_COLOR

        # Button shadow
        shadow_rect = start_button.move(3, 3)
        shadow_surf = pygame.Surface((start_button.w, start_button.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, SHADOW_COLOR, (0, 0, start_button.w, start_button.h), border_radius=12)
        screen.blit(shadow_surf, shadow_rect)

        # Button main
        pygame.draw.rect(screen, button_color, start_button, border_radius=12)

        # Gloss effect
        highlight = pygame.Surface((start_button.w, start_button.h // 2), pygame.SRCALPHA)
        pygame.draw.rect(
            highlight,
            (255, 255, 255, 50),
            (0, 0, start_button.w, start_button.h // 2),
            border_radius=12
        )
        screen.blit(highlight, (start_button.x, start_button.y))

        # Button text
        button_text = button_font.render("START GAME", True, (20, 30, 25))
        button_text_main = button_font.render("START GAME", True, TEXT_COLOR)
        text_rect = button_text.get_rect(center=start_button.center)
        screen.blit(button_text, (text_rect.x + 1, text_rect.y + 1))
        screen.blit(button_text_main, text_rect)

        # Instructions
        instruction_text = SMALL_FONT1.render("Press any key or click the button to start", True, (200, 220, 200))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5))
        screen.blit(instruction_text, instruction_rect)

        # Footer
        copyright_lines = [
            "Created by:", "Yasssine Boussabat", "Adem Ben Neji", "Nourhene Ayari", "Farah fatouhi"
        ]
        line_spacing = 30
        for i, line in enumerate(copyright_lines):
            line_surf = SMALL_FONT1.render(line, True, COPYRIGHT_COLOR)
            line_rect = line_surf.get_rect(center=(WIDTH // 2, HEIGHT - 220 + i * line_spacing))
            screen.blit(line_surf, line_rect)

        pygame.display.flip()

class SudokuGUI:
    def __init__(self):
        self.sudoku = None
        self.solution = None
        self.selected_cell = None  
        self.cell_size = GRID_SIZE // 9 
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = "easy"  
        self.algorithm = "hill"  
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
        self.grid_y = 105

        # Boutons
        self.create_buttons()

    def create_buttons(self):
        button_width = 78  
        button_height = 30
        spacing = 80     
        
        # Boutons de difficulté
        self.difficulty_buttons = {
            "easy": pygame.Rect(25, 20, button_width, button_height),
            "medium": pygame.Rect(25 + button_width + spacing, 20, button_width, button_height),
            "hard": pygame.Rect(25 + 2*(button_width + spacing), 20, button_width, button_height),
            "expert": pygame.Rect(25 + 3*(button_width + spacing), 20, button_width, button_height)
        }

        # Boutons d'algorithme
        self.algorithm_buttons = {
            "hill": pygame.Rect(spacing + 40, 65, button_width, button_height),
            "astar": pygame.Rect(160 + button_width + spacing*2, 65, button_width, button_height)
        }

        # Bouton Résoudre
        self.solve_button = pygame.Rect(WIDTH - 130, 680, button_width, button_height)
        
        # Bouton Réinitialiser
        self.reset_button = pygame.Rect(WIDTH - 260, 680, button_width, button_height)

    def display_grid(self):
        window.fill(WHITE)

        # Dessiner la grille 9x9
        for i in range(10):
            
            pygame.draw.line(
                window, 
                BLACK, 
                (self.grid_x + i * self.cell_size, self.grid_y), 
                (self.grid_x + i * self.cell_size, self.grid_y + GRID_SIZE), 
                3 if i % 3 == 0 else 1
            )
           
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
                    color = GREEN1
                    if self.selected_cell == (row, col):
                        color = RED
                    elif self.solution and self.solution[row][col] != self.grid[row][col]:
                        color = GREEN  
                    
                    num_text = FONT2.render(str(number), True, color)
                    window.blit(
                        num_text, 
                        (self.grid_x + col * self.cell_size + self.cell_size // 3, 
                         self.grid_y + row * self.cell_size - 7 + self.cell_size // 4)
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
        
        window.blit(status_text, (30, HEIGHT - 85))
        window.blit(SMALL_FONT.render(f"Iterations: {self.iterations}", True, BLACK), (30, HEIGHT - 65))
        window.blit(SMALL_FONT.render(f"Conflicts: {self.conflicts}", True, BLACK), (30, HEIGHT - 45))
        window.blit(SMALL_FONT.render(f"Time: {self.execution_time:.3f} sec", True, BLACK), (30, HEIGHT - 25))

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
        
        ACTIVE_COLOR = (100, 255, 100)  
        INACTIVE_COLOR = (50, 50, 80)    
        HOVER_COLOR = (70, 130, 180)     
        TEXT_COLOR = (240, 240, 240)    
        SHADOW_COLOR = (20, 20, 40, 150) 
        
        # Draw difficulty buttons
        for name, rect in self.difficulty_buttons.items():
            
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            active = self.difficulty == name
            
            
            base_color = ACTIVE_COLOR if active else (HOVER_COLOR if hovered else INACTIVE_COLOR)
            
            
            shadow_rect = rect.move(3, 3)
            shadow_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, SHADOW_COLOR, (0, 0, rect.w, rect.h), border_radius=8)
            window.blit(shadow_surf, shadow_rect)
            
            
            pygame.draw.rect(window, base_color, rect, border_radius=8)
            
            
            highlight_rect = rect.inflate(-6, -6)
            pygame.draw.rect(window, (*base_color[:3], 50), highlight_rect, border_radius=5)
            
              
            btn_text = name.capitalize()
            text_surface = BUTTON_FONT.render(btn_text, True, (30, 30, 30))  
            text_rect = text_surface.get_rect(center=rect.center) 
            window.blit(text_surface, (text_rect.x + 2, text_rect.y + 2))
            text_surface = BUTTON_FONT.render(btn_text, True, TEXT_COLOR)
            window.blit(text_surface, text_rect)
        
        # Draw algorithm buttons 
        for name, rect in self.algorithm_buttons.items():
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            active = self.algorithm == name
            base_color = ACTIVE_COLOR if active else (HOVER_COLOR if hovered else INACTIVE_COLOR)
            
            
            shadow_rect = rect.move(3, 3)
            shadow_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, SHADOW_COLOR, (0, 0, rect.w, rect.h), border_radius=8)
            window.blit(shadow_surf, shadow_rect)
            
            
            pygame.draw.rect(window, base_color, rect, border_radius=8)
            
            
            highlight_rect = rect.inflate(-6, -6)
            pygame.draw.rect(window, (*base_color[:3], 50), highlight_rect, border_radius=5)
            
           
            btn_text = "Hill" if name == "hill" else "A*"
            text_surface = BUTTON_FONT.render(btn_text, True, (30, 30, 30))  
            text_rect = text_surface.get_rect(center=rect.center) 
            window.blit(text_surface, (text_rect.x + 2, text_rect.y + 2))
            text_surface = BUTTON_FONT.render(btn_text, True, TEXT_COLOR)
            window.blit(text_surface, text_rect)
        
        # Solve button 
        solve_hovered = self.solve_button.collidepoint(pygame.mouse.get_pos())
        solve_color = (100, 220, 100) if solve_hovered else (80, 180, 80)
        
        
        shadow_rect = self.solve_button.move(3, 3)
        shadow_surf = pygame.Surface((self.solve_button.w, self.solve_button.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, SHADOW_COLOR, (0, 0, self.solve_button.w, self.solve_button.h), border_radius=8)
        window.blit(shadow_surf, shadow_rect)
        
        
        pygame.draw.rect(window, solve_color, self.solve_button, border_radius=8)
        
       
        highlight_rect = self.solve_button.inflate(-6, -6)
        pygame.draw.rect(window, (*solve_color[:3], 50), highlight_rect, border_radius=5)
        
       
        solve_text = BUTTON_FONT.render("SOLVE", True, (30, 30, 30))  
        solve_text_main = BUTTON_FONT.render("SOLVE", True, (240, 255, 240))  
        text_rect = solve_text.get_rect(center=self.solve_button.center)
        window.blit(solve_text, (text_rect.x + 2, text_rect.y + 2))
        window.blit(solve_text_main, text_rect)
        
        # Reset button 
        reset_hovered = self.reset_button.collidepoint(pygame.mouse.get_pos())
        reset_color = (255, 100, 100) if reset_hovered else (220, 80, 80)
        
        
        shadow_rect = self.reset_button.move(3, 3)
        shadow_surf = pygame.Surface((self.reset_button.w, self.reset_button.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, SHADOW_COLOR, (0, 0, self.reset_button.w, self.reset_button.h), border_radius=8)
        window.blit(shadow_surf, shadow_rect)
        
        
        pygame.draw.rect(window, reset_color, self.reset_button, border_radius=8)
        
        
        highlight_rect = self.reset_button.inflate(-6, -6)
        pygame.draw.rect(window, (*reset_color[:3], 50), highlight_rect, border_radius=5)
        
        
        reset_shadow = BUTTON_FONT.render("RESET", True, (30, 30, 30))  
        reset_main = BUTTON_FONT.render("RESET", True, (255, 200, 200))  
        text_rect = reset_shadow.get_rect(center=self.reset_button.center)
        window.blit(reset_shadow, (text_rect.x + 2, text_rect.y + 2))
        window.blit(reset_main, text_rect)

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
            original_grid = [row[:] for row in self.grid]
            self.sudoku = Sudoku(self.grid)
            
            start_time = time.time()
            
            if self.algorithm == "hill":
                solver = HillClimbingSolver(self.sudoku)
                self.solution, self.iterations, self.conflicts = solver.solve()
            elif self.algorithm == "astar":
                self.solution, self.iterations = astar_solver(self.sudoku)
                self.conflicts = 0
            
            self.execution_time = time.time() - start_time
            
            if not self.solution:
                self.error_message = "No solution found!"
                return
            
            if self.conflicts == 0:
                self.solved = True
            else:
                self.solved = False
            
            self.grid = original_grid
            
            self.animate_solution()
                    
        except Exception as e:
            self.error_message = f"Solving error: {str(e)}"

    def animate_solution(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0: 
                    empty_cells.append((i, j))
        
        import random
        random.shuffle(empty_cells)
        
        self.cells_to_animate = empty_cells
        self.animation_index = 0
        self.animation_speed = 2 
        self.animation_active = True
        
        # Glow effect variables
        self.glowing_cells = {}  
        self.glow_duration = 30  
        self.glow_intensity = 255 
        
        self.original_display_grid = self.display_grid
        self.display_grid = self.display_grid_with_animation

    def display_grid_with_animation(self):

        window.fill(WHITE)
        
        for i in range(10):
            pygame.draw.line(
                window, 
                BLACK, 
                (self.grid_x + i * self.cell_size, self.grid_y), 
                (self.grid_x + i * self.cell_size, self.grid_y + GRID_SIZE), 
                3 if i % 3 == 0 else 1
            )

            pygame.draw.line(
                window, 
                BLACK, 
                (self.grid_x, self.grid_y + i * self.cell_size), 
                (self.grid_x + GRID_SIZE, self.grid_y + i * self.cell_size), 
                3 if i % 3 == 0 else 1
            )
        
        for (row, col), intensity in list(self.glowing_cells.items()):
            glow_color = (0, intensity, 0)  
            
            cell_rect = pygame.Rect(
                self.grid_x + col * self.cell_size + 1, 
                self.grid_y + row * self.cell_size + 1,
                self.cell_size - 2, 
                self.cell_size - 2
            )
            
            pygame.draw.rect(window, glow_color, cell_rect)
            
            new_intensity = intensity - (255 / self.glow_duration)
            if new_intensity <= 0:
                
                del self.glowing_cells[(row, col)]
            else:
                
                self.glowing_cells[(row, col)] = new_intensity
        
        for row in range(9):
            for col in range(9):
                number = self.grid[row][col]
                if number != 0:
                    color = GREEN1
                    if self.selected_cell == (row, col):
                        color = RED
                    elif self.solution and self.solution[row][col] != number:
                        color = GREEN  
                    
                    num_text = FONT2.render(str(number), True, color)
                    window.blit(
                        num_text, 
                        (self.grid_x + col * self.cell_size + self.cell_size // 3, 
                        self.grid_y + row * self.cell_size - 7 + self.cell_size // 4)
                    )
        
        self.draw_buttons()
        self.display_results()
        
        # Display error messages
        if self.error_message:
            error_text = SMALL_FONT.render(self.error_message, True, RED)
            window.blit(error_text, (10, HEIGHT - 90))
        
        pygame.display.flip()
        
        if self.animation_active:

            for _ in range(self.animation_speed):
                if self.animation_index < len(self.cells_to_animate):
                    i, j = self.cells_to_animate[self.animation_index]
                    self.grid[i][j] = self.solution[i][j]
                    self.glowing_cells[(i, j)] = self.glow_intensity
                    self.animation_index += 1
                else:
                    
                    if not self.glowing_cells:
                        self.animation_active = False
                        self.display_grid = self.original_display_grid
                    break


def main():
    show_welcome_screen()
    sudoku_gui = SudokuGUI()
    sudoku_gui.reset_grid()  

    while sudoku_gui.running:
        sudoku_gui.handle_input()
        sudoku_gui.display_grid()
        sudoku_gui.clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()