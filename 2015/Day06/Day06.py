from helper import aoc_timer
import re
import numpy as np
from matplotlib import pyplot as plt


def get_input(path):
    for line in open(path).read().split('\n'):
        result = re.search(
            r"(on|off|toggle) (\d+),(\d+) through (\d+),(\d+)", line
        ).groups()
        op, r1, c1, r2, c2 = result
        yield op, [slice(int(r1), int(r2) + 1), slice(int(c1), int(c2) + 1)]


@aoc_timer
def Day06(path, part1=True, plot=False):
    # Initialise lights grid
    G = np.zeros((1000, 1000), dtype=int)

    # Instructions differ by part (p)
    instr = {
        'on': lambda x, p: 1 if p else x + 1,
        'off': lambda x, p: 0 if p else np.where((x - 1) < 0, 0, (x - 1)),
        'toggle': lambda x, p: x ^ 1 if p else x + 2
    }

    # Apply instructions to grid
    for op, coords in get_input(path):
        G[coords] = instr[op](G[coords], part1)

    # Matplotlib plot
    if plot:
        if part1:
            cmap = 'Greys'
        else:
            cmap = 'viridis'
        plt.figure()
        plt.imshow(G, cmap=cmap)
        plt.axis('off')

    return G.sum()


# %% Output
def main():
    print("AoC 2015\nDay 06")
    path = 'input.txt'
    print("Part 1:", Day06(path, part1=True, plot=True))
    print("Part 2:", Day06(path, part1=False, plot=True))


if __name__ == '__main__':
    main()
