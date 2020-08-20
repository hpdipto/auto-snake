import pygame, sys, time, datetime
from pygame.locals import *
import numpy as np


# set up the window
WINDOWWIDTH = 700
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH+40, WINDOWHEIGHT+40), 0, 32)
pygame.display.set_caption('RL Snake')


# set up the direction variable
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
MOVESPEED = 20


# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


# function for checking the collision of an object with snake mouth
def collid_with_snake_mouth(snake_mouth, obj):

	# function for checking if x in [a, b]
	def in_range(x, a, b):
		if x >= a and x <= b:
			return True
		return False

	# check for all four possible point of snake_mouth
	if in_range(snake_mouth.left+1, obj.left, obj.right) and in_range(snake_mouth.top+1, obj.top, obj.bottom):
		return True
	if in_range(snake_mouth.left+1, obj.left, obj.right) and in_range(snake_mouth.bottom-1, obj.top, obj.bottom):
		return True
	if in_range(snake_mouth.right-1, obj.left, obj.right) and in_range(snake_mouth.top+1, obj.top, obj.bottom):
		return True
	if in_range(snake_mouth.right-1, obj.left, obj.right) and in_range(snake_mouth.bottom-1, obj.top, obj.bottom):
		return True

	# if in_range(snake_mouth.left+1, obj.left, obj.right):
	# 	return True
	# if in_range(snake_mouth.bottom-1, obj.top, obj.bottom):
	# 	return True
	# if in_range(snake_mouth.right-1, obj.left, obj.right):
	# 	return True
	# if in_range(snake_mouth.top+1, obj.top, obj.bottom):
	# 	return True

	return False




# function for checking if the snake cross the boundary or not
def cross_boundary(snake_mouth, WINDOWWIDTH, WINDOWHEIGHT):
	if snake_mouth.top < 20:
		return True
	if snake_mouth.left < 20:
		return True
	if snake_mouth.bottom > WINDOWHEIGHT+20:
		return True
	if snake_mouth.right > WINDOWWIDTH+20:
		return True
	return False



# function for controlling the body of snake
def snake_move(snake_body, command):
	snake_mouth = snake_body[0].copy()

	if command == RIGHT:
		snake_mouth.right += MOVESPEED
	if command == LEFT:
		snake_mouth.left -= MOVESPEED
	if command == UP:
		snake_mouth.top -= MOVESPEED
	if command == DOWN:
		snake_mouth.bottom += MOVESPEED

	snake = [snake_mouth] + snake_body[:len(snake_body)-1]
	return snake



# function for increasing snake direction when snake eat a food
def increase_snake(snake_body, direction):
	if direction == RIGHT:
		new_snake = pygame.Rect(snake_body[-1].left-20, snake_body[-1].top, 20,20)
	if direction == LEFT:
		new_snake = pygame.Rect(snake_body[-1].left, snake_body[-1].top, 20, 20)
	if direction == DOWN:
		new_snake = pygame.Rect(snake_body[-1].left, snake_body[-1].top-20, 20, 20)
	if direction == UP:
		new_snake = pygame.Rect(snake_body[-1].left, snake_body[-1].top, 20, 20)

	snake_body.append(new_snake)
	return snake_body
