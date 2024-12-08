# %% Day 05
from helper import aoc_timer
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

type Data = tuple[dict[int, set[int]], list[int]]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        R = defaultdict(set)
        rules, updates = f.read().split("\n\n")
        for r in rules.splitlines():
            a, b = map(int, r.split("|"))
            R[a].add(b)
        U = [[*map(int, line.split(","))] for line in updates.splitlines()]
        return R, U


@aoc_timer
def solve(data: Data) -> tuple[int, int]:
    R, U = data

    @dataclass
    class Page(int):
        value: int

        def __lt__(self, other: Self) -> bool:
            return other.value in R[self.value]

    p1 = p2 = 0
    for update in U:
        mid = len(update) // 2
        update = [*map(Page, update)]
        if (new := sorted(update)) == update:
            p1 += update[mid]
        else:
            p2 += new[mid]
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 05")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
