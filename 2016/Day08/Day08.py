from helper import aoc_timer
import numpy as np
import re


OP = {
    'D': lambda screen, a, b: draw(screen, a, b),
    'R': lambda screen, a, b: rotate_rows(screen, a, b),
    'C': lambda screen, a, b: rotate_cols(screen, a, b)
}


@aoc_timer
def get_input(path):
    for line in open(path).readlines():
        a, b = map(int, re.findall(r'\d+', line))
        if line.startswith('rect'):
            op = 'D'
        elif line.startswith('rotate row'):
            op = 'R'
        elif line.startswith('rotate col'):
            op = 'C'
        else:
            assert False, "Unexpected input."
        yield op, a, b


def draw(screen, a, b):
    screen[:b, :a] = 1
    return screen


def rotate_rows(screen, a, b):
    screen[a] = np.roll(screen[a], b)
    return screen


def rotate_cols(screen, a, b):
    screen[:, a] = np.roll(screen[:, a], b)
    return screen


@aoc_timer
def Day08(data):
    R, C = 6, 50
    p1, p2 = 0, '\n'
    screen = np.zeros((R, C), dtype=int)
    for op, a, b in data:
        screen = OP[op](screen, a, b)
    p1 = np.sum(screen)
    for r in range(len(screen)):
        for c in range(len(screen[r])):
            if screen[r, c] == 1:
                p2 += '#'
            else:
                p2 += ' '
        p2 += '\n'
    return p1, p2


# %% Output
def main():
    print("AoC 2016\nDay 08")
    data = get_input('input.txt')
    p1, p2 = Day08(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
