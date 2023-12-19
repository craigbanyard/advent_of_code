# %% Day 14
from helper import aoc_timer
import itertools as it
import numpy as np


@aoc_timer
def get_input(path: str) -> np.ndarray:
    return np.array([[*line] for line in open(path).read().splitlines()])


def render(platform: np.ndarray) -> str:
    '''Return a string representation of the platform.'''
    return '\n'.join(''.join(line) for line in platform)


def tilt(platform: np.ndarray, R: int) -> np.ndarray:
    '''Tilt the platform upwards (north).'''
    for r, c in state(platform):
        while 0 <= (rr := r - 1) < R and platform[rr][c] == '.':
            platform[rr][c] = 'O'
            platform[r][c] = '.'
            r -= 1
    return platform


def state(platform: np.ndarray, ch: str = 'O') -> tuple[tuple[int]]:
    '''Return a hashable state of elements of the platform equal to `ch`.'''
    return tuple((r, c) for r, c in zip(*np.where(platform == ch)))


def load(rounded: tuple[tuple[int]], R: int) -> int:
    '''Return the load on the north support beam.'''
    return int(sum(R - r for r, _ in rounded))


@aoc_timer
def solve(p: np.ndarray, lim: float = 0.25) -> int:
    R = len(p)
    loads, seen = {}, {}
    cycle = 0
    for d in it.cycle(range(4)):
        p = tilt(p, R)
        q = np.rot90(p, d)
        cycle += 0.25
        if (s := state(q)) in seen:
            start = seen[s]
            _, r = divmod(lim - start, cycle - start)
            return loads[start + r]
        seen[s] = cycle
        loads[cycle] = load(s, R)
        if cycle == lim:
            return loads[cycle]
        p = np.rot90(p, 3)


def main() -> None:
    print("AoC 2023\nDay 14")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, lim=1000000000))


if __name__ == '__main__':
    main()
