from helper import aoc_timer
import numpy as np
import re


@aoc_timer
def get_input(path):
    return [list(map(int, re.findall(r'\d+', line)))
            for line in open(path).readlines()]


@aoc_timer
def Day05(data, n, part1=True):
    G = np.zeros((n, n), dtype=int)
    for x1, y1, x2, y2 in data:
        if x1 != x2 and y1 != y2:
            if part1:
                continue
            # Diagonal lines
            dx, dy = map(np.sign, (x2 - x1, y2 - y1))
            for c, r in zip(range(x1, x2 + dx, dx), range(y1, y2 + dy, dy)):
                G[r][c] += 1
            continue
        # Horizontal and vertical lines
        G[min(y1, y2):max(y1, y2) + 1, min(x1, x2):max(x1, x2) + 1] += 1
    return np.sum(G > 1)


# %% Output
def main():
    print("AoC 2021\nDay 05")
    data = get_input('input.txt')
    n = np.max(data) + 1
    print("Part 1:", Day05(data, n, part1=True))
    print("Part 2:", Day05(data, n, part1=False))


if __name__ == '__main__':
    main()
