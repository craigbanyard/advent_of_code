# %% Day 03
from helper import aoc_timer
from collections import defaultdict
import itertools as it
from math import prod


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


@aoc_timer
def solve(data: list[str]) -> tuple[int]:
    R = len(data)
    C = len(data[0])
    N = set('0123456789.')
    S = set(''.join(data)) - N
    D = [
        (-1, -1),   # Up-left
        (-1, 0),    # Up
        (-1, 1),    # Up-right
        (0, -1),    # Left
        (0, 1),     # Right
        (1, -1),    # Down-left
        (1, 0),     # Down
        (1, 1),     # Down-right
    ]

    def valid(r: int, c: int) -> bool:
        '''
        Determine whether a position is within the grid and is a
        numeric digit.
        '''
        return 0 <= r < R and 0 <= c < C and data[r][c].isdigit()

    p1, p2 = 0, 0
    symbols = defaultdict(list)
    for r, c in it.product(range(R), range(C)):
        if data[r][c] not in S:
            continue
        visited = set()
        for dr, dc in D:
            if not valid(rr := r + dr, cc := c + dc):
                continue
            if (rr, cc) in visited:
                continue
            visited.add((rr, cc))
            n = data[rr][cc]
            for d in [-1, 1]:
                while valid(rr, cc := cc + d):
                    if (rr, cc) in visited:
                        continue
                    visited.add((rr, cc))
                    m = data[rr][cc]
                    n = m + n if d == -1 else n + m
            symbols[(data[r][c], r, c)].append(int(n))
    for (s, *_), parts in symbols.items():
        p1 += sum(parts)
        if s == '*' and len(parts) == 2:
            p2 += prod(parts)
    return p1, p2


def main() -> None:
    print("AoC 2023\nDay 03")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
