import value_propagation_func as vpf
import rlf
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
snake = [pygame.Rect(60, 20, 20, 20), pygame.Rect(40, 20, 20, 20), pygame.Rect(20, 20, 20, 20)]
snake_direction = RIGHT


# set up boundary
boundary = pygame.Rect(20, 20, WINDOWWIDTH, WINDOWHEIGHT)



# run the main loop
if __name__ == "__main__":

	game_over = False
	score = 0

	# set up food, food position will always be a multiple of 20
	possible_food = list(range(20, 701, 20))
	food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)


	# get policy for the generated food
	policy = vpf.get_policy(snake, food)

	while True:
		# check for the QUIT event
		for e in pygame.event.get():
			if e.type == QUIT:
				pygame.quit()
				sys.exit()


		# get direction from policy
		row, col = int(snake[0].top / 20), int(snake[0].left / 20)
		# if policy[row, col] != 0:
		snake_direction = policy[row, col]

		# draw the white background onto the surface
		windowSurface.fill(WHITE)

		# movement according to direction
		if snake_direction == RIGHT:
			snake = rlf.snake_move(snake, RIGHT)
		elif snake_direction == LEFT:
			snake = rlf.snake_move(snake, LEFT)
		elif snake_direction == UP:
			snake = rlf.snake_move(snake, UP)
		elif snake_direction == DOWN:
			snake = rlf.snake_move(snake, DOWN)
		# print(snake_direction)


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
		if rlf.collid_with_snake_mouth(snake[0], food) == True:
			# defining new food and increase snake size
			food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)
			# make it sure that the food doesn't generate inside snake body
			while food in snake:
				food = pygame.Rect(np.random.choice(possible_food), np.random.choice(possible_food[:25]), 20, 20)
			rlf.increase_snake(snake, snake_direction)

			# increasing score
			score += 1
			score_str = "Score: " + str(score)


			# write the row and column of generated food into a text file
			row, col = int(food.top / 20), int(food.left / 20)

			# get new policy for new food
			policy = vpf.get_policy(snake, food)
			#print(policy)


		# if collision happened with itself
		for i in range(3, len(snake)):
			if rlf.collid_with_snake_mouth(snake[0], snake[i]) == True:
				game_over = True
				print("Collid with self!")
				print(food)
				print(grid3d)
				break

		# if cross boundary
		if rlf.cross_boundary(snake[0], WINDOWWIDTH, WINDOWHEIGHT) == True:
			print("Boundary Crossed!")
			game_over = True
			
		#draw the window onto the screen if the game not over
		if game_over == False:
			pygame.display.update()
			time.sleep(0.08)
