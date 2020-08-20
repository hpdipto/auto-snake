import pygame, sys, time, datetime
from pygame.locals import *
import numpy as np

# set up pygame
pygame.init()

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

# set up font and rectangle for holding text
font = pygame.font.SysFont(None, 30)
end_font = pygame.font.SysFont(None, 80)
textRect = pygame.Rect(20, 0, 100, 20)
score_str = "Score: 0"

# set up snake
snake = [pygame.Rect(60, 20, 20, 20), pygame.Rect(40, 20, 20, 20), pygame.Rect(20, 20, 20, 20)]
snake_direction = RIGHT


# set up boundary
boundary = pygame.Rect(20, 20, WINDOWWIDTH, WINDOWHEIGHT)


# set up food, food position will always be a multiple of 20
possible_food = list(range(20, 701, 20))
food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)


# function for checking the collision of an object with snake mouth
def collid_with_snake_mouth(snake_mouth, obj):
	collid = False

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
game_over = False
score = 0
while True:
	# check for the QUIT event
	for e in pygame.event.get():
		if e.type == QUIT:
			pygame.quit()
			sys.exit()

		# key board control
		elif e.type == KEYDOWN:
			if e.key == K_RIGHT and (snake_direction == UP or snake_direction == DOWN):
				snake_direction = RIGHT
			elif e.key == K_LEFT and (snake_direction == UP or snake_direction == DOWN):
				snake_direction = LEFT
			elif e.key == K_UP and (snake_direction == LEFT or snake_direction == RIGHT):
				snake_direction = UP
			elif e.key == K_DOWN and (snake_direction == LEFT or snake_direction == RIGHT):
				snake_direction = DOWN

	# draw the white background onto the surface
	windowSurface.fill(WHITE)

	# movement according to direction
	if snake_direction == RIGHT:
		snake = snake_move(snake, RIGHT)
	elif snake_direction == LEFT:
		snake = snake_move(snake, LEFT)
	elif snake_direction == UP:
		snake = snake_move(snake, UP)
	elif snake_direction == DOWN:
		snake = snake_move(snake, DOWN)


	# if the game over - we take this pain of come back to the loop again for having a good end display :(
	if game_over == True:
		pygame.draw.rect(windowSurface, BLACK, boundary, 1)
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
		food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)
		# make it sure that the food doesn't generate inside snake body
		while food in snake:
			food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)
		increase_snake(snake, snake_direction)

		# increasing score
		score += 1
		score_str = "Score: " + str(score)


	# if collision happened with itself
	for i in range(3, len(snake)):
		if collid_with_snake_mouth(snake[0], snake[i]) == True:
			game_over = True
			break

	# if cross boundary
	if cross_boundary(snake[0], WINDOWWIDTH, WINDOWHEIGHT) == True:
		game_over = True

	#draw the window onto the screen if the game not over
	if game_over == False:
		pygame.display.update()
		time.sleep(0.08)
