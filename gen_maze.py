import numpy as np
import random

def gen_maze_prim(num_rows, num_cols):  # 扭曲迷宫
	# (行坐标，列坐标，四面墙的有无&访问标记)
    m = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)
    r, c = 0, 0
    trace = [(r, c)]
    while trace:
        r, c = random.choice(trace)
        m[r, c, 4] = 1	# 标记为通路
        trace.remove((r, c))
        check = []
        if c > 0:
            if m[r, c - 1, 4] == 1:
                check.append('L')
            elif m[r, c - 1, 4] == 0:
                trace.append((r, c - 1))
                m[r, c - 1, 4] = 2	# 标记为已访问
        if r > 0:
            if m[r - 1, c, 4] == 1:
                check.append('U')
            elif m[r - 1, c, 4] == 0:
                trace.append((r - 1, c))
                m[r - 1, c, 4] = 2
        if c < num_cols - 1:
            if m[r, c + 1, 4] == 1:
                check.append('R')
            elif m[r, c + 1, 4] == 0:
                trace.append((r, c + 1))
                m[r, c + 1, 4] = 2
        if r < num_rows - 1:
            if m[r + 1, c, 4] == 1:
                check.append('D')
            elif m[r + 1, c, 4] == 0:
                trace.append((r + 1, c))
                m[r + 1, c, 4] = 2
        if len(check):
            direction = random.choice(check)
            if direction == 'L':	# 打通一面墙
                m[r, c, 0] = 1
                c = c - 1
                m[r, c, 2] = 1
            if direction == 'U':
                m[r, c, 1] = 1
                r = r - 1
                m[r, c, 3] = 1
            if direction == 'R':
                m[r, c, 2] = 1
                c = c + 1
                m[r, c, 0] = 1
            if direction == 'D':
                m[r, c, 3] = 1
                r = r + 1
                m[r, c, 1] = 1
    m[0, 0, 0] = 1
    m[num_rows - 1, num_cols - 1, 2] = 1
    return m

def gen_maze_dfs(num_rows, num_cols):  # 曲折迷宫
    m = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)
    r = 0
    c = 0
    trace = [(r, c)]
    while trace:
        m[r, c, 4] = 1  # 标记为已访问
        check = []
        if c > 0 and m[r, c - 1, 4] == 0:
            check.append('L')
        if r > 0 and m[r - 1, c, 4] == 0:
            check.append('U')
        if c < num_cols - 1 and m[r, c + 1, 4] == 0:
            check.append('R')
        if r < num_rows - 1 and m[r + 1, c, 4] == 0:
            check.append('D')
        if len(check):
            trace.append([r, c])
            direction = random.choice(check)
            if direction == 'L':
                m[r, c, 0] = 1
                c = c - 1
                m[r, c, 2] = 1
            if direction == 'U':
                m[r, c, 1] = 1
                r = r - 1
                m[r, c, 3] = 1
            if direction == 'R':
                m[r, c, 2] = 1
                c = c + 1
                m[r, c, 0] = 1
            if direction == 'D':
                m[r, c, 3] = 1
                r = r + 1
                m[r, c, 1] = 1
        else:
            r, c = trace.pop()
    m[0, 0, 0] = 1
    m[num_rows - 1, num_cols - 1, 2] = 1
    return m


def gen_maze(num_size, flag):
    maze = []
    for i in range(2*num_size+1):
        maze.append([0] * (2*num_size+1))
    m = np.zeros((num_size, num_size, 5), dtype=np.uint8)
    if flag == "prim":
        m = gen_maze_prim(num_size, num_size)
    elif flag == "dfs":
        m = gen_maze_dfs(num_size, num_size)
    else:
        return maze
    for i in range(num_size):
        ni = 2*i+1
        for j in range(num_size):
            nj = 2*j+1
            maze[ni-1][nj-1] = maze[ni-1][nj+1] = maze[ni+1][nj+1] = maze[ni+1][nj-1] = 1
            info = m[i][j]
            if info[0] == 0:  #  left
                maze[ni][nj-1] = 1 # wall
            if info[1] == 0: #  up
                maze[ni-1][nj] = 1
            if info[2] == 0: #  right
                maze[ni][nj+1] = 1
            if info[3] == 0: #  down
                maze[ni+1][nj] = 1
    maze[1][0] = 2
    maze[2*num_size-1][2*num_size] = 3
    return maze

def print_maze(maze):
    for line in maze:
        print(line)
    print()


if __name__ == "__main__":
    maze = gen_maze(5, "dfs")
    print_maze(maze)
    maze = gen_maze(5, "prim")
    print_maze(maze)
