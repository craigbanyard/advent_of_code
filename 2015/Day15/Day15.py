from helper import aoc_timer
import re
import numpy as np


def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def parse(x, delims):
    return list(map(to_int, re_split(delims, x.strip())[1:]))


@aoc_timer
def get_input(path):
    delims = [': capacity ', ', durability ', ', flavor ', ', texture ', ', calories ']
    return {x.split(':')[0]: parse(x, delims) for x in open(path).readlines()}


@aoc_timer
def Day15(data, part2=False):

    ing = data.copy()
    cal = []

    # Put calories in separate list
    for k, v in ing.items():
        ing[k] = v[:-1]
        cal.append(v[-1])

    ans = 0
    tsp = 100
    kcal = 500

    for a in range(tsp+1):
        for b in range(tsp+1-a):
            for c in range(tsp+1-a-b):
                d = tsp-a-b-c
                if part2:
                    cals = sum(x*y for x, y in zip([a, b, c, d], cal))
                    if cals != kcal:
                        continue
                temp = [max(0, a*p + b*q + c*r + d*s) for p, q, r, s in zip(*ing.values())]
                ans = max(ans, np.prod(temp))
    return ans


# %% Output
def main():
    print("AoC 2015\nDay 15")
    data = get_input('input.txt')
    print("Part 1:", Day15(data))
    print("Part 2:", Day15(data, part2=True))


if __name__ == '__main__':
    main()
