from helper import aoc_timer
from time import sleep
from os import getcwd


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


@aoc_timer
def Day03(data, slopes, part1=True, p1_data=None):
    rows, cols = len(data), len(data[0])
    prod = p1_data or 1
    for dr, dc in slopes:
        c, collisions = 0, 0
        for r in range(dr, rows, dr):
            if data[r][(c := (c + dc) % cols)] == '#':
                collisions += 1
        prod *= collisions
    if part1:
        return collisions
    return prod


def Day03_vis(data, slopes, wait=0.05):
    rows, cols = len(data), len(data[0])
    for dr, dc in slopes:
        c, collisions = 0, 0
        print(data[0])
        for r in range(dr, rows, dr):
            c = (c + dc) % cols
            line = data[r][:c]
            if data[r][c] == '#':
                collisions += 1
                line += f'X{data[r][c+1:]}    Ouch: {collisions}'
            else:
                line += f'O{data[r][c+1:]}'
            print(line)
            sleep(wait)
        print('\n' + '=' * 80 + '\n')


# %% Output
def main():
    print("AoC 2020\nDay 3")
    path = getcwd() + "\\Inputs\\Day03.txt"
    data = get_input(path)
    p1 = Day03(data, [(1, 3)])
    print("Part 1:", p1)
    print("Part 2:", Day03(data, [(1, 1), (1, 5), (1, 7), (2, 1)], False, p1))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
212 µs ± 967 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day03(data, [(1, 3)], True)
57.5 µs ± 133 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day03(data, [(1, 1), (1, 5), (1, 7), (2, 1)], False, p1)
199 µs ± 2.73 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
'''
