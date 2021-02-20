from helper import aoc_timer
import re


@aoc_timer
def get_input(path):
    return open(path).read()


def sum_json(j):
    """RegEx on string input"""
    return sum(map(int, re.findall(r'-?\d+', j)))


def filter_json(j, item):
    """Recursive sum on JSON input where property != item"""
    if isinstance(j, int):
        return j
    if isinstance(j, list):
        return sum([filter_json(i, item) for i in j])
    if not isinstance(j, dict):
        return 0
    if item in j.values():
        return 0
    return filter_json(list(j.values()), item)


@aoc_timer
def Day12(data, part1=True):
    if part1:
        return sum_json(data)
    j = eval(data)
    return filter_json(j, 'red')


# %% Output
def main():
    print("AoC 2015\nDay 12")
    data = get_input('input.txt')
    print("Part 1:", Day12(data))
    print("Part 2:", Day12(data, part1=False))


if __name__ == '__main__':
    main()
