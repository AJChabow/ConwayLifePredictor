import pygame
import sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
# Constants
WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 30 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

grid = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = WHITE if grid[x][y] else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))



def get_neighbors(x, y, grid):
    neighbors = []
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    
    rows, cols = len(grid), len(grid[0])
    
    for dx, dy in offsets:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols: # making sure in bounds
            neighbors.append(grid[nx][ny]) # add list of neighbours
    return neighbors

def takestep():
    global grid
    global running
    newgrid = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            neighbours = get_neighbors(x, y, grid)
            near_pop = sum(neighbours)
            
            if grid[x][y] == 0 and near_pop == 3:
                newgrid[x][y] = 1
            elif grid[x][y] == 1:
                if near_pop < 2 or near_pop > 3:
                    newgrid[x][y] = 0
                else:
                    newgrid[x][y] = 1

                    
    if grid == newgrid: # stop condition
        running = False
    else:
        grid = newgrid

running = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x //= CELL_SIZE
            y //= CELL_SIZE
            grid[x][y] = 1 - grid[x][y]
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and running:
                print("Stopping")
                running = False
            elif event.key == K_SPACE:
                print("Starting")
                running = True
            elif event.key == K_r:
                print("Resetting")
                grid = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
            
    if running:
        takestep()
        FPS = 30
    else:
        FPS = 30

    screen.fill(BLACK)
    draw_grid()

    pygame.display.flip()
    clock.tick(FPS)
