from time import time, sleep
import numpy as np
from scipy.signal import correlate2d

path = "F:\\Users\\Craig\\Documents\\Programming\\Python\\Advent of Code\\2015\\Inputs\\Day18.txt"

def get_input(path):
    return [x.strip() for x in open(path).readlines()]

def adj(data,pos,part=1):
    if part == 2 and pos in [(0,0),(0,99),(99,0),(99,99)]:
        return '#'
    r,c = pos
    counter = 0
    current = 1 if data[r][c] == '#' else 0
    # Clockwise from upper-left
    dR = [-1,-1,-1,0,1,1,1,0]
    dC = [-1,0,1,1,1,0,-1,-1]
    for dr,dc in zip(dR,dC):
        if any(x in [-1,100] for x in [r+dr,c+dc]):
            continue
        if data[r+dr][c+dc] == '#':
            counter += 1
            if counter > 3:
                return '.'
    if current:
        return '#' if counter in [2,3] else '.'
    return '#' if counter == 3 else '.'

def Day18(data,steps,part=1,vis=False):
    R, C = len(data), len(data[0])
    for t in range(steps):
        nxt = ['' for _ in range(R)]
        for r in range(R):
            for c in range(C):
                nxt[r] += adj(data,(r,c),part)
        data = nxt
    if vis:
        return data
    return sum(sum(map(line.count,'#')) for line in data)

# Want to find a way to animate this in a new window, overwriting the grid each step
def animate(data,steps):
    for t in range(steps+1):
        for line in data:
            print(line)
        sleep(0.5)
        data = Day18(data,1,1,1)
        print()


# %% Using NumPy/SciPy - holy shit the SPEED!

grid = np.zeros((100,100),bool)
for r, line in enumerate(open(path)):
    grid[r][[i for i, ch in enumerate(line) if ch == '#']] = 1

# This uses torroidal geometry - i.e. wraps around edges
def update(grid):
    adjacents = sum(np.roll(np.roll(grid, i, 0), j, 1)
                    for i in (-1,0,1) for j in (-1,0,1)
                    if (i != 0 or j !=0))
    return (adjacents == 3) | grid & (adjacents == 2)

# This uses fixed boundary
def new_state_v(grid,part):
    kernel = np.ones((3,3))
    kernel[1,1] = 0
    neighbours = correlate2d(grid, kernel, 'same')
    nxt = grid.copy()
    nxt[(grid == 1) & ((neighbours < 2) | (neighbours > 3))] = 0
    nxt[(grid == 0) & (neighbours == 3)] = 1
    if part == 2:
        nxt[::nxt.shape[0]-1, ::nxt.shape[1]-1] = 1
    return nxt

# Play the Game of Life
def gol(data,steps=100,part=1):
    # Create NumPy array of bools from input grid
    grid = np.zeros((100,100),bool)
    for r, line in enumerate(open(path)):
        grid[r][[i for i, ch in enumerate(line) if ch == '#']] = 1
    # Play the game
    for t in range(steps):
        grid = new_state_v(grid,part)
    return np.sum(grid)

# %% Output
print("AoC 2015\nDay 18\n-----")
t0=time()
data = get_input(path)
steps = 1
print("Data:",time()-t0,"\n-----")
t0=time()
print("Part 1:",Day18(data,steps))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",Day18(data,steps,2))
print("Time:",time()-t0,"\n-----")