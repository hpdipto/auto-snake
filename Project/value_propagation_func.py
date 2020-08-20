import numpy as np
import rlf
import pygame, sys, time, datetime
from pygame.locals import *
# import value_prop_test_1 as vpt1

def distance_from_object(x1, y1, x2, y2):
    """Calculate distance and direction from point (x1, y1), (x2, y2)
       Return: distance from - X-axis, Y-axis; direction to X-axis, Y-axis"""
    
    x_distance = abs(x1 - x2)
    if x_distance == 0:
        x_direction = None
    else:
        x_direction = rlf.RIGHT if x2 > x1 else rlf.LEFT

    y_distance = abs(y1 - y2)
    if y_distance == 0:
        y_direction = None
    else:
        y_direction = rlf.DOWN if y2 > y1 else rlf.UP

    return (x_distance, y_distance, x_direction, y_direction)


def grid_init(snake, food):

    # grid3d - initialize with 0 to store the Q-value
    grid3d = np.zeros((27, 37, 5), dtype='float64')

    # upgrade grid3d with punishment and reward
    for i in range(1, len(snake)):
        sn = snake[i]
        row, col = int(sn.top / 20), int(sn.left / 20)
        grid3d[row, col] = -10.0

    row, col = int(food.top / 20), int(food.left / 20)
    grid3d[row, col] = 10.0

    return grid3d


    
def border_distance(x1, y1):
    """Calculate distance of a block from border
       Return: distance from - UP, BOTTOM, LEFT, RIGHT"""

    distance_from_up = y1
    distance_from_bottom = 26 - y1

    distance_from_left = x1
    distance_from_right = 36 - x1

    return (distance_from_up, distance_from_bottom, distance_from_right, distance_from_left)



def value_propagation(grid3d, snake, food, row_length=26, col_length=36, reward=10, punishment=-10, discount=0.01):
    for row in range(1, row_length):
        for col in range(1, col_length):

            # don't upgrade reward or punishment grids
            if np.sum(grid3d[row, col]) != 0:
                continue

            # propagating punishment for border
            u, d, r, l = border_distance(col, row)   # row, col exchanged; amazing bug!!!
            grid3d[row,col, rlf.UP] += ( punishment * discount ** u)
            grid3d[row,col, rlf.DOWN] += ( punishment * discount ** d)
            grid3d[row,col, rlf.RIGHT] += ( punishment * discount ** r)
            grid3d[row,col, rlf.LEFT] += ( punishment * discount ** l)

            # start debuging from here!!!
            # propagating punishment for snake body
            for i in range(1, len(snake)):
                snake_row, snake_col = int(snake[1].top / 20), int(snake[1].left / 20)
                x_dis, y_dis, x_dir, y_dir = distance_from_object(row, col, snake_row, snake_col)
                if x_dir != None:
                    grid3d[row, col, x_dir] += (punishment * discount ** x_dis)
                if y_dir != None:
                    grid3d[row, col, y_dir] += (punishment * discount ** y_dis)

            # propagating reward for food
            food_row, food_col = int(food.top / 20), int(food.left / 20)
            x_dis, y_dis, x_dir, y_dir = distance_from_object(row, col, food_row, food_col)
            if x_dir != None:
                grid3d[row, col, x_dir] += (reward * discount ** x_dis)
            if y_dir != None:
                grid3d[row, col, y_dir] += (reward * discount ** y_dis)

    return grid3d


def print_grid(grid3d):
    for row in range(1, len(grid3d)-1):
        for col in range(1, len(grid3d[row])-1):
            for height in range(1, len(grid3d[row, col])):
                print("%.2f"%grid3d[row, col, height], end=",")
            print(end=" ")
        print(end="\n")


    
def get_policy(snake, food, row=27, col=37):
    grid3d = grid_init(snake, food)
    grid3d = value_propagation(grid3d, snake, food)
    
    policy = np.zeros((row, col))
    r, c = int(food.top / 20), int(food.left / 20)
    
    for r in range(len(grid3d)):
        for c in range(len(grid3d[r])):
            policy[r, c] = np.argmax(grid3d[r][c])

    return policy

# snake = [pygame.Rect(60, 20, 20, 20), pygame.Rect(40, 20, 20, 20), pygame.Rect(20, 20, 20, 20)]
# possible_food = list(range(20, 701, 20))
# food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)

# policy = get_policy(snake, food, 27, 37)
