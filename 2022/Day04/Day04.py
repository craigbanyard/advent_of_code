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
        s1 = range(a, b + 1)
        s2 = range(c, d + 1)
        if (intersection := range(max(a, c), min(b, d) + 1)):
            p2 += 1
        if intersection == s1 or intersection == s2:
            p1 += 1
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
