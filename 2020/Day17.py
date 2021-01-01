from helper import aoc_timer
from os import getcwd
import numpy as np
from scipy.ndimage import correlate


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def get_grid(data, dims=3):
    N = len(data)
    grid = np.zeros((N, N), dtype=int)
    for r, line in enumerate(data):
        grid[r][[i for i, ch in enumerate(line) if ch == '#']] = 1
    d = [1] * (dims - 2) + [N] * 2
    return grid.reshape(d)


def pad_grid(grid):
    return np.pad(grid, [(1,)], mode='constant', constant_values=0)


def evolve(grid, dims=3):
    grid = pad_grid(grid)
    kernel = np.ones([3] * dims)
    np.put(kernel, kernel.size // 2, 0)
    nei = correlate(grid, kernel, mode='constant', cval=0)
    nxt = grid.copy()
    nxt[(grid == 1) & ((nei < 2) | (nei > 3))] = 0
    nxt[(grid == 0) & (nei == 3)] = 1
    return nxt


@aoc_timer
def Day17(data, steps=6, dims=3):
    if dims < 2:
        return 0
    grid = get_grid(data, dims)
    for t in range(steps):
        grid = evolve(grid, dims)
    return np.sum(grid)


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day17.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day17.txt"
    print("AoC 2020\nDay 17")
    data = get_input(path)
    print("Part 1:", Day17(data, steps=6, dims=3))
    print("Part 2:", Day17(data, steps=6, dims=4))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
124 µs ± 262 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day17(data, steps=6, dims=3)
1.39 ms ± 3.38 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day17(data, steps=6, dims=4)
13.8 ms ± 110 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
'''
