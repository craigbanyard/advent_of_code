# %% Day 13
from helper import aoc_timer
import itertools as it
import numpy as np
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[np.ndarray]:
    for pattern in open(path).read().split('\n\n'):
        yield np.array([[x == '#' for x in line]
                        for line in pattern.splitlines()])


def summarise(p: np.ndarray, f: int = 100, seen: int = 0) -> int:
    '''Summarise pattern p, skipping if the result has already been seen.'''
    for idx, (a, b) in enumerate(zip(p, p[1:])):
        if not np.array_equal(a, b) or (idx + 1) * f == seen:
            continue
        for c, d in zip(p[idx - 1::-1], p[idx + 2:]):
            if not np.array_equal(c, d) and idx > 0:
                break
        else:
            return (idx + 1) * f
    if f == 1:
        return 0
    return summarise(p.T, f=1, seen=seen)


@aoc_timer
def solve(data: Iterator[np.ndarray]) -> tuple[int]:
    p1, p2 = 0, 0
    for p in data:
        a = summarise(p)
        for r, c in it.product(*map(range, np.shape(p))):
            q = np.copy(p)
            q[r][c] = ~q[r][c]
            if (b := summarise(q, seen=a)) and b != a:
                p2 += b
                break
        p1 += a
    return p1, p2


def main() -> None:
    print("AoC 2023\nDay 13")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
