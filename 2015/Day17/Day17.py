from helper import aoc_timer
from itertools import combinations


@aoc_timer
def get_input(path):
    return [int(x.strip()) for x in open(path).readlines()]


@aoc_timer
def Day17(data, target=150):
    p1 = [
        cmb for r in range(len(data), 0, -1)
        for cmb in combinations(data, r)
        if sum(cmb) == target
    ]
    p2 = [1 for cmb in p1 if len(cmb) == min(map(len, p1))]
    return len(p1), len(p2)


# %% Output
def main():
    print("AoC 2015\nDay 17")
    data = get_input('input.txt')
    p1, p2 = Day17(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
