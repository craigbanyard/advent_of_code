# %% Day 02
from helper import aoc_timer
import itertools as it
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[list[int]]:
    with open(path) as f:
        yield from [[*map(int, line.split())] for line in f.read().splitlines()]


def safe(report: list[int]) -> bool:
    d = set(a - b for a, b in it.pairwise(report))
    return d.issubset({1, 2, 3}) or d.issubset({-1, -2, -3})


@aoc_timer
def solve(data: list[list[int]]) -> tuple[int, int]:
    p1, p2 = 0, 0
    for report in data:
        if safe(report):
            p1 += 1
            continue
        for idx in range(len(report)):
            if safe(report[:idx] + report[idx + 1:]):
                p2 += 1
                break
    return p1, p1 + p2


def main() -> None:
    print("AoC 2024\nDay 02")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
