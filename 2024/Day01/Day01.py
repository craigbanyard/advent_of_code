# %% Day 01
from helper import aoc_timer
from collections import Counter


@aoc_timer
def get_input(path: str) -> list[list[int]]:
    with open(path) as f:
        return [[*map(int, line.split())] for line in f.read().splitlines()]


@aoc_timer
def solve(data: list[list[int]]) -> tuple[int, int]:
    L, R = zip(*data)
    left, right = map(Counter, (L, R))
    p1, p2 = 0, 0
    for a, b in zip(*map(sorted, (L, R))):
        p1 += abs(a - b)
        p2 += a * left.pop(a, 0) * right[a]
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 01")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
