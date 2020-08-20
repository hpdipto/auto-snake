import numpy as np
import rlf
import value_iteration_func as vif
# import snake_manual as sm
import automated as atmd


def value_iteration_init(row, col, snake):

    # grid3d - where all possible q-value will be stored
    grid3d = np.zeros((27, 37, 5))

    # grid_reward - stores reward or punishment
    grid_reward = np.zeros((27, 37))

    # grid
    grid = np.zeros((27, 37))

    # reward_position - stores the position of the reward and punishment
    reward_position = list()

    # policy - policy for each grid
    policy = np.zeros((27, 37))


    grid_reward[row, col] = 100
    reward_position.append((row, col))

    # get snake body position, extract required row and column and store as punishment grid
    for block in snake:
        if block == snake[0]:
            continue
        row = int(block.top / 20)
        col = int(block.left / 20)
        grid_reward[row, col] = -100
        reward_position.append((row, col))

    # set punishment on the border
    for i in range(0, 27, 1):
        for j in range(0, 37, 1):
            if i == 0 or j == 0 or i == 26 or j == 36:
                grid_reward[i, j] = -100
                reward_position.append((i, j))

    # set grid as get_reward
    # grid = grid_reward.copy()

    # set discount
    discount = 0.1

    return policy, grid, grid3d, grid_reward, reward_position, discount


# iteration for getting grid values
def value_iteration(policy, grid, grid3d, grid_reward, reward_position, discount):
    for row in range(0, 27, 1):
        for col in range(0, 37, 1):
            if grid_reward[row, col] != 0:
                continue
            # if (row, col) in reward_position:
            #     continue
            # move UP
            if row-1 >= 0:
                grid3d[row, col, rlf.UP] = (grid_reward[row-1, col] + discount * grid[row-1, col])

            # move DOWN
            if row+1 <= 26:
                grid3d[row, col, rlf.DOWN] = (grid_reward[row+1, col] + discount * grid[row+1, col])

            # move RIGHT
            if col+1 <= 36:
                grid3d[row, col, rlf.RIGHT] = (grid_reward[row, col+1] + discount * grid[row, col+1])

            # move LEFT
            if col-1 >= 0:
                grid3d[row, col, rlf.LEFT] = (grid_reward[row, col-1] + discount * grid[row, col-1])

    for row in range(0, 27, 1):
        for col in range(0, 37, 1):
            # if (row, col) in reward_position:
            #     continue
            if grid_reward[row, col] != 0:
                continue
            grid[row, col] = np.max(grid3d[row, col])
            policy[row, col] = np.argmax(grid3d[row, col])
            # if grid[row, col] < 0:
            #     policy[row, col] = 0

    return policy, grid


def get_policy(policy, grid, grid3d, reward_position):
    for row in range(0, 27, 1):
        for col in range(0, 37, 1):
            if (row, col) in reward_position:
                continue
            grid[row, col] = np.max(grid3d[row, col])
            policy[row, col] = np.argmax(grid3d[row, col])

    return policy

if __name__ == "__main__":
    policy, grid, grid3d, grid_reward, reward_position, discount = value_iteration_init(23, 23)
    for i in range(0, 100):
        policy = value_iteration(policy, grid, grid3d, grid_reward, reward_position, discount)

    print(grid)
    print("====================================")
    print(policy)
