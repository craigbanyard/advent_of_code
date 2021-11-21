import collections
from helper import aoc_timer
from collections import Counter


@aoc_timer
def get_input(path):
    return [x for x in zip(*open(path).readlines())]


@aoc_timer
def Day06(data):
    p1, p2 = '', ''
    for column in data:
        (a, _), *_, (b, _) = Counter(column).most_common()
        p1 += a
        p2 += b
    return p1, p2


# %% Output
def main():
    print("AoC 2016\nDay 06")
    data = get_input('input.txt')
    p1, p2 = Day06(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
