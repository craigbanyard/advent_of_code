from helper import aoc_timer
import re


@aoc_timer
def get_input(path):
    return map(int, re.findall(r'\d+', open(path).read()))


def row_start(r):
    """nth term of arithmetic sequence:
        1, 2, 4, 7, 11, 16, ...
        n(n-1)/2 + 1
    """
    return (r * (r-1)) // 2 + 1


def elem_num(r, c):
    """Element number at position (r, c)"""
    return row_start(r + c) - r


@aoc_timer
def Day25(data):
    R, C = data
    seed = 20151125
    g = 252533
    p = 33554393
    e = elem_num(R, C) - 1
    return (seed * pow(g, e, p) % p)


# %% Output
def main():
    print("AoC 2015\nDay 25")
    data = get_input('input.txt')
    print("Day 25:", Day25(data))


if __name__ == '__main__':
    main()
