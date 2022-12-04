from helper import aoc_timer
import re
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[list[int]]:
    for line in open(path).read().splitlines():
        yield list(map(int, re.findall(r'\d+', line)))


@aoc_timer
def solve(data: Iterator[list[int]]) -> tuple[int, int]:
    p1, p2 = 0, 0
    for a, b, c, d in data:
        if c >= a and d <= b or a >= c and b <= d:
            p1 += 1
        if max(a, c) <= min(b, d):
            p2 += 1
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 04")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
