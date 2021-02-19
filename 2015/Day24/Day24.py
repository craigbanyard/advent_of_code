from helper import aoc_timer
from functools import reduce
from itertools import combinations
from operator import mul


@aoc_timer
def get_input(path):
    return [int(x.strip()) for x in open(path).readlines()]


@aoc_timer
def Day24(data, num_groups):
    target_sum = sum(data) // num_groups
    for i in range(len(data)):
        qes = [reduce(mul, c) for c in combinations(data, i) if sum(c) == target_sum]
        if qes:
            return min(qes)


# %% Output
def main():
    print("AoC 2015\nDay 24")
    data = get_input('input.txt')
    print("Part 1:", Day24(data, 3))
    print("Part 2:", Day24(data, 4))


if __name__ == '__main__':
    main()
