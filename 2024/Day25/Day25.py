# %% Day 25
from helper import aoc_timer
import itertools as it
from typing import Self

type Data = tuple[list[Schematic], list[Schematic]]


class Schematic:
    R = 5
    C = 5

    def __init__(self, schematic: str) -> None:
        self.heights = [-1] * self.C
        for line in schematic.splitlines():
            for idx, ch in enumerate(line):
                self.heights[idx] += ch == "#"
        self.lock = ch == "."

    def fits(self, other: Self) -> bool:
        for idx in range(self.C):
            if self.heights[idx] + other.heights[idx] > self.R:
                return False
        return True


@aoc_timer
def get_input(path: str) -> Data:
    locks, keys = [], []
    with open(path) as f:
        for schematic in map(Schematic, f.read().split("\n\n")):
            (keys, locks)[schematic.lock].append(schematic)
    return locks, keys


@aoc_timer
def solve(data: Data) -> int:
    return sum(key.fits(lock) for lock, key in it.product(*data))


def main() -> None:
    print("AoC 2024\nDay 25")
    data = get_input("input.txt")
    print("Part 1:", solve(data))


if __name__ == "__main__":
    main()
