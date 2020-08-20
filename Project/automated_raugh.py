import pygame, sys, time, datetime
from pygame.locals import *
import numpy as np

import snake_body


# set up pygame
pygame.init()

score = 0

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
key_mapping = {'UP': 1, 'DOWN': 2, 'RIGHT': 3, 'LEFT': 4, 'MOVESPEED': 20}


# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# set up font and rectangle for holding text
font = pygame.font.SysFont(None, 30)
end_font = pygame.font.SysFont(None, 80)
textRect = pygame.Rect(20, 0, 100, 20)
score_str = "Score: 0"

# set up snake
snake_mouth = pygame.Rect(5, 5, 20, 20)
snake = [pygame.Rect(60, 20, 20, 20), pygame.Rect(40, 20, 20, 20), pygame.Rect(20, 20, 20, 20)]
snake_direction = RIGHT


# set up boundary
boundary = pygame.Rect(20, 20, WINDOWWIDTH, WINDOWHEIGHT)


# set up food
food = pygame.Rect(np.random.randint(20, 700), np.random.randint(20, 500), 20, 20)


# function for checking the collision of an object with snake mouth
def collid_with_snake_mouth(snake_mouth, obj):
	collid = False

	# function for checking if (x, y) inside obj or not
	def point_inside_object(x, y, obj):
		if (x >= obj.left and x <= obj.right) and (y >= obj.top and y <= obj.bottom):
			return True
		return False

	if point_inside_object(snake_mouth.left, snake_mouth.top, obj):
		collid = True
	if point_inside_object(snake_mouth.left, snake_mouth.bottom, obj):
		collid = True
	if point_inside_object(snake_mouth.right, snake_mouth.top, obj):
		collid = True
	if point_inside_object(snake_mouth.right, snake_mouth.bottom, obj):
		collid = True
	
	return collid

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


# run the main loop
command_file = open("hello.txt", "r")

for line in command_file:
	snake_direction = key_mapping[line.split(' ')[0]]
	distance = int(line.split(' ')[1])
	while True:
		# check for the QUIT event
		for e in pygame.event.get():
			if e.type == QUIT:
				pygame.quit()
				sys.exit()
			
			# key board control
			# elif e.type == KEYDOWN:
			# 	if e.key == K_RIGHT and (snake_direction == UP or snake_direction == DOWN):
			# 		snake_direction = RIGHT
			# 	elif e.key == K_LEFT and (snake_direction == UP or snake_direction == DOWN):
			# 		snake_direction = LEFT
			# 	elif e.key == K_UP and (snake_direction == LEFT or snake_direction == RIGHT):
			# 		snake_direction = UP
			# 	elif e.key == K_DOWN and (snake_direction == LEFT or snake_direction == RIGHT):
			# 		snake_direction = DOWN

		# draw the white background onto the surface
		windowSurface.fill(WHITE)

		# movement according to direction
		if snake_direction == RIGHT:
			snake = snake_move(snake, RIGHT)
			if snake[0].left >= distance:
				break
		elif snake_direction == LEFT:
			snake = snake_move(snake, LEFT)
			if snake[0].right <= distance:
				break
		elif snake_direction == UP:
			snake = snake_move(snake, UP)
			if snake[0].bottom <= distance:
				break
		elif snake_direction == DOWN:
			snake = snake_move(snake, DOWN)
			if snake[0].top >= distance:
				break

		# drawing snake, food, boundary and writing score
		s_color = RED
		for block in snake:
			pygame.draw.rect(windowSurface, s_color, block)
			s_color = GREEN

		pygame.draw.rect(windowSurface, BLUE, food)
		pygame.draw.rect(windowSurface, BLACK, boundary, 1)
		text = font.render(score_str, True, BLACK, None)
		windowSurface.blit(text, textRect)
		

		# if collision happened with food
		if collid_with_snake_mouth(snake[0], food) == True:
			# defining new food and increase snake size
			food = pygame.Rect(np.random.randint(20, 700), np.random.randint(20, 500), 20, 20)
			# make it sure that the food doesn't generate inside snake body
			while food in snake:
				food = pygame.Rect(np.random.randint(20, 700), np.random.randint(20, 500), 20, 20)
			increase_snake(snake, snake_direction)

			# increasing score
			score += 1
			score_str = "Score: " + str(score)

		
		# if collision happened with itself
		for i in range(3, len(snake)):
			if collid_with_snake_mouth(snake[0], snake[i]) == True:
				pygame.display.update()
				end_text = "Game Over! Score: " + str(score)
				end_text = end_font.render(end_text, True, BLACK, None)
				end_textRect = end_text.get_rect()
				end_textRect.centerx = windowSurface.get_rect().centerx
				end_textRect.centery = windowSurface.get_rect().centery
				windowSurface.blit(end_text, end_textRect)
				pygame.display.update()
				time.sleep(3)
				pygame.quit()
				sys.exit()

		# if cross boundary
		if cross_boundary(snake[0], WINDOWWIDTH, WINDOWHEIGHT) == True:
			end_text = "Game Over! Score: " + str(score)
			end_text = end_font.render(end_text, True, BLACK, None)
			end_textRect = end_text.get_rect()
			end_textRect.centerx = windowSurface.get_rect().centerx
			end_textRect.centery = windowSurface.get_rect().centery
			windowSurface.blit(end_text, end_textRect)
			pygame.display.update()
			time.sleep(3)
			pygame.quit()
			sys.exit()
		
		#draw the window onto the screen
		pygame.display.update()
		time.sleep(0.08)
