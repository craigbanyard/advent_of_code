from helper import aoc_timer
import numpy as np
from scipy.ndimage import correlate


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def get_grid(data, dims=2):
    N = len(data)
    grid = np.zeros((N, N), dtype=int)
    for r, line in enumerate(data):
        grid[r][[i for i, ch in enumerate(line) if ch == '#']] = 1
    d = [1] * (dims - 2) + [N] * 2
    return grid.reshape(d)


def pad_grid(grid):
    return np.pad(grid, [(1,)], mode='constant', constant_values=0)


def evolve(grid, dims=2, bounded=True, part2=False):
    if not bounded:
        grid = pad_grid(grid)
    kernel = np.ones([3] * dims)
    np.put(kernel, kernel.size // 2, 0)
    nei = correlate(grid, kernel, mode='constant', cval=0)
    nxt = grid.copy()
    nxt[(grid == 1) & ((nei < 2) | (nei > 3))] = 0
    nxt[(grid == 0) & (nei == 3)] = 1
    if dims == 2 and part2:
        nxt[tuple(slice(None, None, j-1) for j in nxt.shape)] = 1
    return nxt


@aoc_timer
def Day18(data, steps=100, dims=2, bounded=True, part2=False):
    if dims < 2:
        return 0
    grid = get_grid(data, dims)
    for t in range(steps):
        grid = evolve(grid, dims, bounded, part2)
    return np.sum(grid)


# %% Output
def main():
    print("AoC 2015\nDay 18")
    data = get_input('input.txt')
    print("Part 1:", Day18(data))
    print("Part 2:", Day18(data, part2=True))


if __name__ == '__main__':
    main()
