# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pygame
import Astar
import Graph
from collections import namedtuple
import Heuristic
import random
import math
import time

class monst:
    def __init__(self, starting_pos, unit_type):
        self.current = starting_pos
        self.unit_type = unit_type
        
    def get_pos(self):
        return self.current
    
    def change_pos(self, next_pos):
        self.current = next_pos

class player:
    def __init__(self, starting_pos):
        self.current_pos = starting_pos
    
    def get_current(self):
        return self.current_pos
    
    def change_pos(self, next_pos):
        self.current_pos = next_pos        

grid_to_node = {}
grid = []
monster = monst((0,0), "Monster")
player = player((5,5))

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
orange   = ( 244, 164, 96)

ROWS = 25
COLUMNS = 25

width  = 20
height = 20


Node = namedtuple('Node', ['x', 'y', 'cost'])
graph = Graph.Graph()



# This sets the margin between each cell
margin = 5

for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        grid[row].append(0)
        
def reset_grid():
    global grid
    for row in range(ROWS):
        for column in range(COLUMNS):
            if grid[row][column] != 3:
                grid[row][column] = 0
    grid[0][0] = 1

player_position = player.get_current()
grid[player_position[0]][player_position[1]] = 4    
grid[0][0] = 1

def draw():
    screen.fill(black)
    grid[player.current_pos[0]][player.current_pos[1]] = 4
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = white
            if grid[row][column] == 1:
                color = red
            elif grid[row][column] == 2:
                color = green
            elif grid[row][column] == 3:
                color = blue
            elif grid[row][column] == 4:
                color = orange
            pygame.draw.rect(screen,
                             color,
                             [(margin+width)*column+margin,
                              (margin+height)*row+margin,
                              width,
                              height])
    # Limit to 20 frames per second
    clock.tick(20)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    

for i in range(int(math.ceil(0.25 * (ROWS * COLUMNS)))):
    highx = random.randint(0, ROWS-1)
    highy = random.randint(0, COLUMNS-1)
    grid[highx][highy] = 3

node_grid = []

for i in range(ROWS):
    node_grid.append([])
    for j in range(COLUMNS):
        if grid[i][j] == 0 or grid[i][j] == 1: 
            node = Node(i,j,1)
        else:
            node = Node(i,j,10000)
        node_grid[i].append(node)
        graph.add_node(node)

for i in range(ROWS):
    for j in range(COLUMNS):
        if j > 0: # has a left neighbor
            graph.add_edge(node_grid[i][j], node_grid[i][j-1])
        if j < COLUMNS-1: # has right neighbor
            graph.add_edge(node_grid[i][j], node_grid[i][j+1])
        if i > 0: # has top neighbor
            graph.add_edge(node_grid[i][j], node_grid[i-1][j])
        if i < ROWS-1: # has bottom neighbor
            graph.add_edge(node_grid[i][j], node_grid[i+1][j])
        if j > 0 and i > 0: # has top left neighbor
            graph.add_edge(node_grid[i][j], node_grid[i-1][j-1])
        if j < COLUMNS-1 and i > 0: # has top right neighbor
            graph.add_edge(node_grid[i][j], node_grid[i-1][j+1])
        if j > 0 and i < ROWS-1: # has bottom left neighbor
            graph.add_edge(node_grid[i][j], node_grid[i+1][j-1])
        if j < COLUMNS-1 and i < ROWS-1: # has bottom right neighbor
            graph.add_edge(node_grid[i][j], node_grid[i+1][j+1])
     
pygame.init()
size = [(width*COLUMNS)+(margin*(COLUMNS+1)), (height*ROWS)+(margin*(ROWS+1))]
screen = pygame.display.set_mode(size)

# Set title of screen
pygame.display.set_caption("Astar Route")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Handle hold down key event

while not done:
    draw()
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if player.current_pos[1] < COLUMNS-1:
                    if grid[player.current_pos[0]][player.current_pos[1] + 1] != 3:
                        player.change_pos((player.current_pos[0], player.current_pos[1] + 1))
                        reset_grid()
                        draw()
            elif event.key == pygame.K_w:
                if player.current_pos[0] > 0:
                    if grid[player.current_pos[0] - 1][player.current_pos[1]] != 3:
                        player.change_pos((player.current_pos[0] - 1, player.current_pos[1]))
                        reset_grid()
                        draw()
            elif event.key == pygame.K_s:
                if player.current_pos[0] < ROWS-1:
                    if grid[player.current_pos[0] + 1][player.current_pos[1]] != 3:
                        player.change_pos((player.current_pos[0] + 1, player.current_pos[1]))
                        reset_grid()
                        draw()
            elif event.key == pygame.K_a:
                if player.current_pos[1] > 0:
                    if grid[player.current_pos[0]][player.current_pos[1] - 1] != 3:
                        player.change_pos((player.current_pos[0], player.current_pos[1] - 1))
                        reset_grid()
                        draw()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            reset_grid()
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            # Set that location to zero
            grid[row][column] = 2
            #print("Click", pos, "Grid coordinates: ", row, column)
            path = Astar.Astar(node_grid[0][0], node_grid[row][column], graph)
            for node in path:
                #print node.x, node.y
                if grid[node.x][node.y] != 3:
                    grid[node.x][node.y] = 2
            grid[0][0] = 1 # color the start red
            for node in path:
                monster.change_pos((node.x, node.y))                                    
                grid[node.x][node.y] = 1
                #time.sleep(2)
                draw()
                

    
    
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

# <codecell>


