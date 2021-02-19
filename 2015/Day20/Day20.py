from helper import aoc_timer
import numpy as np


@aoc_timer
def get_input(path):
    return int(open(path).read())


@aoc_timer
def Day20(N):
    upper = 1000000  # Educated guess at upper-limit
    np1 = np.full((upper), 10, dtype=int)  # Part 1
    np2 = np.full((upper), 10, dtype=int)  # Part 2
    for i in range(2, upper):
        np1[i::i] += 10 * i
        np2[i:(50*i)+1:i] += 11 * i
    return np.min(np.where(np1 > N)), np.min(np.where(np2 > N))


# %% Output
def main():
    print("AoC 2015\nDay 20")
    data = get_input('input.txt')
    p1, p2 = Day20(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
