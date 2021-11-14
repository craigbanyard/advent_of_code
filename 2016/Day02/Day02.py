from helper import aoc_timer
import numpy as np


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def get_keypad(part1):
    # Part 1 keypad and starting position
    P1 = np.arange(1, 10).reshape(3, 3)
    pos1 = np.array([1, 1])

    # Part 2 keypad and starting position
    P2 = np.array([
        [0, 0, 1, 0, 0],
        [0, 2, 3, 4, 0],
        [5, 6, 7, 8, 9],
        [0, 'A', 'B', 'C', 0],
        [0, 0, 'D', 0, 0]
    ])
    pos2 = np.array([2, 0])

    # Return keypad and start position for current part
    if part1:
        return P1, pos1
    return P2, pos2


@aoc_timer
def Day02(data, part1=True):
    D = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)

    }
    P, pos = get_keypad(part1)
    lb, ub = 0, len(P) - 1
    code = ''
    for line in data:
        for i in line:
            tmp = np.clip(pos + D[i], lb, ub)
            if P[tuple(tmp)] == '0':
                continue
            pos = tmp
        code += str(P[tuple(pos)])
    return code


# %% Output
def main():
    print("AoC 2016\nDay 02")
    data = get_input('input.txt')
    print("Part 1:", Day02(data))
    print("Part 2:", Day02(data, part1=False))


if __name__ == '__main__':
    main()
