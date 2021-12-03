from helper import aoc_timer
from collections import Counter
import numpy as np


@aoc_timer
def get_input(path):
    return np.array([*zip(*open(path).readlines())])


@aoc_timer
def part1(data):
    gamma = epsilon = ''
    for column in data:
        (a, _), (b, _) = Counter(column).most_common()
        gamma += a
        epsilon += b
    return int(gamma, 2) * int(epsilon, 2)


@aoc_timer
def part2(data):
    oxy = co2 = np.transpose(data)
    ofound = cfound = False
    idx = 0
    while not (ofound and cfound):
        if not (ofound := len(oxy) == 1):
            ocol = oxy[:, idx]
            (a, m), (b, n) = Counter(ocol).most_common()
            if m == n:
                a = '1'
            oxy = oxy[np.where(ocol == a)]
        if not (cfound := len(co2) == 1):
            ccol = co2[:, idx]
            (a, m), (b, n) = Counter(ccol).most_common()
            if m == n:
                b = '0'
            co2 = co2[np.where(ccol == b)]
        idx += 1
    return int(''.join(oxy[0]), 2) * int(''.join(co2[0]), 2)


# %% Output
def main():
    print("AoC 2021\nDay 03")
    data = get_input('input.txt')
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == '__main__':
    main()
