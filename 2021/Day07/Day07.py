from helper import aoc_timer
import numpy as np


@aoc_timer
def get_input(path):
    return np.array([*open(path).read().split(',')], dtype=int)


@aoc_timer
def Day07(data):

    def fuel(n):
        return n * (n -1) // 2

    lo, hi = np.min(data), np.max(data)
    p1 = p2 = np.inf
    for n in range(lo, hi + 1):
        df = np.abs(n - data)
        p1 = min(p1, df.sum())
        p2 = min(p2, np.vectorize(fuel)(df + 1).sum())
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 07")
    data = get_input('input.txt')
    p1, p2 = Day07(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
