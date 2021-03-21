from helper import aoc_timer
import numpy as np
from scipy.ndimage import correlate


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def get_grid(data):
    """Convert ASCII list into numpy binary array."""
    N = len(data)
    grid = np.zeros((N, N), dtype=int)
    for r, line in enumerate(data):
        grid[r][[i for i, ch in enumerate(line) if ch == '#']] = 1
    return grid


def evolve(grid):
    """Perform one timestep grid evolution."""
    kernel = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ], dtype=int)
    nei = correlate(grid, kernel, mode='constant', cval=0)
    nxt = grid.copy()
    nxt[(grid == 0) & ((nei == 1) | (nei == 2))] = 1
    nxt[(grid == 1) & (nei != 1)] = 0
    return nxt


def bio(grid):
    """Calculate biodiversity rating of a layout grid."""
    return grid.flatten().dot(1 << np.arange(grid.size))


@aoc_timer
def Day24(data, part1=True):
    G = get_grid(data)
    seen = set()
    while True:
        b = bio(G)
        if b in seen:
            return b
        seen.add(b)
        G = evolve(G)


# %% Output
def main():
    print("AoC 2019\nDay 24")
    data = get_input('input.txt')
    print("Part 1:", Day24(data))
    # print("Part 2:", Day24(data, part1=False))


if __name__ == '__main__':
    main()
