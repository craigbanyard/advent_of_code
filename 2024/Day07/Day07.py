# %% Day 07
from helper import aoc_timer
import itertools as it
import math
from operator import add, mul
import re
from typing import Callable, Iterator


@aoc_timer
def get_input(path: str) -> Iterator[list[int]]:
    with open(path) as f:
        yield from [
            [*map(int, re.findall(r"\d+", line))] for line in f.read().splitlines()
        ]


def concat(a: int, b: int) -> int:
    return a * 10 ** int(math.log10(b) + 1) + b


def insert_ops(eq: list[int], ops: list[Callable]) -> int:
    target, first, *rest = eq
    for ops in it.product(ops, repeat=len(rest)):
        ans = first
        for op, n in zip(ops, rest):
            ans = op(ans, n)
            if ans > target:
                break
        if ans == target:
            return ans
    return 0


@aoc_timer
def solve(data: Iterator[list[int]]) -> tuple[int, int]:
    p1 = p2 = 0
    for eq in data:
        if ans := insert_ops(eq, [add, mul]):
            p1 += ans
        else:
            p2 += insert_ops(eq, [add, mul, concat])
    return p1, p1 + p2


def main() -> None:
    print("AoC 2024\nDay 07")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()