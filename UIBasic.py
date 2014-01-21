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

treasures = {}
treasures_left = 0
level = 1
amount = 2
caught = False
score = 0
monster_list = []

def eaten():
    global caught, score
    caught = True
    screen.fill(black)
    print "You have been caught! :("
    print score

class monst:
    def __init__(self, starting_pos):
        self.current = starting_pos
        
    def get_pos(self):
        return self.current
    
    def change_pos(self, next_pos):
        self.current = next_pos
        
    def track(self, player):
        #reset_grid()
        path = Astar.Astar(node_grid[self.current[0]][self.current[1]], node_grid[player[0]][player[1]], graph)
        if len(path) > 1:
            self.change_pos((path[1].x, path[1].y))
        else:
            self.change_pos((player[0], player[1]))
            eaten()

class player:
    def __init__(self, starting_pos):
        self.current_pos = starting_pos
    
    def get_current(self):
        return self.current_pos
    
    def change_pos(self, next_pos):
        self.current_pos = next_pos        

move = 0 
grid_to_node = {}
grid = []
player = player((5,5))

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
yellow   = ( 255, 255,   0)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
orange   = ( 244, 164, 96)

ROWS = 25
COLUMNS = 25

width  = 20
height = 20

# This sets the margin between each cell
margin = 5

Node = namedtuple('Node', ['x', 'y', 'cost'])
graph = Graph.Graph()

pygame.init()
size = [(width*COLUMNS)+(margin*(COLUMNS+1)), (height*ROWS)+(margin*(ROWS+1))]
screen = pygame.display.set_mode(size)


#image = pygame.image.load("images/cartoon-clown-fish.png").convert()
#image = pygame.transform.scale(image, (20, 20))

for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        grid[row].append(0)

def reset_grid():
    global grid
    for row in range(ROWS):
        for column in range(COLUMNS):
            if grid[row][column] != 3 and grid[row][column] != 2:
                grid[row][column] = 0

player_position = player.get_current()
grid[player_position[0]][player_position[1]] = 4

def draw():  
    global image, treasures, monster_list
    screen.fill(black)
    grid[player.current_pos[0]][player.current_pos[1]] = 4
    for key in treasures:
        if treasures[key] == 0:
            grid[key[0]][key[1]] = 2
    for monster in monster_list:
        grid[monster.current[0]][monster.current[1]] = 1
    #print monster.current
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = white
            if grid[row][column] == 1:
                color = red
            elif grid[row][column] == 2:
                color = yellow
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
    
def init_treasure(amount):
    global treasures, treasures_left
    for i in range(amount):
        treasurex = random.randint(0, ROWS-1)
        treasurey = random.randint(0, COLUMNS-1)
        grid[treasurex][treasurey] = 2
        treasures[(treasurex, treasurey)] = 0
    treasures_left = amount
        
def treasure_check(coords):
    global treasures, treasures_left, level, amount, score
    for key in treasures:
        if coords[0] == key[0] and coords[1] == key[1] and treasures[key] == 0:
            score += 1
            treasures[key] = 1
            treasures_left -= 1
    if treasures_left == 0:
        print "Level Completed!!"
        level += 1
        print level
        level_up()
        
def level_up():
    global monster_list, amount
    amount += 2
    init_treasure(amount)
    monster = monst((random.randint(0, ROWS-1), random.choice([0,COLUMNS-1])))
    monster_list.append(monster)

node_grid = []

for i in range(ROWS):
    node_grid.append([])
    for j in range(COLUMNS):
        if grid[i][j] == 0 or grid[i][j] == 1 or grid[i][j] == 2 or grid[i][j] == 4: 
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
     


# Set title of screen
pygame.display.set_caption("Astar Route")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Level up!
level_up()

while not caught:
    draw()
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
            caught = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if player.current_pos[1] < ROWS-1:
                    if grid[player.current_pos[0]][player.current_pos[1] + 1] != 3:
                        player.change_pos((player.current_pos[0], player.current_pos[1] + 1))
                        treasure_check((player.current_pos[0], player.current_pos[1]))
                        if move == 1:
                            for monster in monster_list:
                                monster.track((player.current_pos[0], player.current_pos[1]))
                            move = 0
                        else:
                            move+=1
                        reset_grid()
                        draw()
            elif event.key == pygame.K_UP:
                if player.current_pos[0] > 0:
                    if grid[player.current_pos[0] - 1][player.current_pos[1]] != 3:
                        player.change_pos((player.current_pos[0] - 1, player.current_pos[1]))
                        treasure_check((player.current_pos[0], player.current_pos[1]))
                        if move == 1:
                            for monster in monster_list:
                                monster.track((player.current_pos[0], player.current_pos[1]))
                            move = 0
                        else:
                            move+=1
                        reset_grid()
                        draw()
            elif event.key == pygame.K_DOWN:
                if player.current_pos[0] < COLUMNS-1:
                    if grid[player.current_pos[0] + 1][player.current_pos[1]] != 3:
                        player.change_pos((player.current_pos[0] + 1, player.current_pos[1]))
                        treasure_check((player.current_pos[0], player.current_pos[1]))
                        if move == 1:
                            for monster in monster_list:
                                monster.track((player.current_pos[0], player.current_pos[1]))
                            move = 0
                        else:
                            move+=1
                        reset_grid()
                        draw()
            elif event.key == pygame.K_LEFT:
                if player.current_pos[1] > 0:
                    if grid[player.current_pos[0]][player.current_pos[1] - 1] != 3:
                        player.change_pos((player.current_pos[0], player.current_pos[1] - 1))
                        treasure_check((player.current_pos[0], player.current_pos[1]))
                        if move == 1:
                            for monster in monster_list:
                                monster.track((player.current_pos[0], player.current_pos[1]))
                            move = 0
                        else:
                            move+=1
                        reset_grid()
                        draw()
                 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

