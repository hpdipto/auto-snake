import numpy as np

grid = np.zeros((36, 26, 5))

def print_grid3d(grid):
    for i in range(1, len(grid)):
        for j in range(1, len(grid[i])):
            for k in range(1, len(grid[i][j])):
                print(grid[i, j, k], end=",")
            print(end="  ")
        print(end="\n")

if __name__ == "__main__":
    print_grid3d(grid)