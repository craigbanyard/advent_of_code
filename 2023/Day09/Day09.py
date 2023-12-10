# %% Day 09
from helper import aoc_timer
import numpy as np


@aoc_timer
def get_input(path: str) -> np.ndarray:
    return np.array(
        [*map(str.split, open(path).read().splitlines())], dtype=int
    )


def extrapolate(seq: np.ndarray) -> int:
    '''Return the next item in the given sequence.'''
    result = seq[-1]
    while not all((seq := np.diff(seq)) == 0):
        result += seq[-1]
    return result


@aoc_timer
def solve(data: np.ndarray) -> int:
    return sum(map(extrapolate, data))


def main() -> None:
    print("AoC 2023\nDay 09")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(np.fliplr(data)))


if __name__ == '__main__':
    main()
