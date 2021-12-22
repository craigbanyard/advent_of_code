from helper import aoc_timer
import numpy as np
import re


INIT = 101


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        op, *coords = re.findall(r'on|off|-?\d+', line)
        yield op == 'on', tuple(map(int, coords))


def translate(coords):
    return tuple(p + INIT // 2 for p in coords)


@aoc_timer
def Day22(data):
    G = np.zeros((INIT, INIT, INIT), dtype=bool)
    for op, coords in data:
        if any(p < -INIT // 2 or p > INIT // 2 for p in coords):
            break
        x1, x2, y1, y2, z1, z2 = translate(coords)
        assert x2 >= x1 and y2 >= y1 and z2 >= z1
        G[x1:x2 + 1, y1:y2 + 1, z1:z2 + 1] = op
    return G.sum(), None


# %% Output
def main():
    print("AoC 2021\nDay 22")
    data = get_input('input.txt')
    # data = get_input('sample.txt')
    # data = get_input('sample2.txt')
    # data = get_input('sample3.txt')
    p1, p2 = Day22(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
