# %% Day 21
from helper import aoc_timer
from collections import defaultdict
from functools import cache
import heapq
import itertools as it
import math


A, U, D, L, R = "A^v<>"
NUM = {
    A: {"0": L, "3": U},
    "0": {A: R, "2": U},
    "1": {"2": R, "4": U},
    "2": {"0": D, "1": L, "3": R, "5": U},
    "3": {A: D, "2": L, "6": U},
    "4": {"1": D, "5": R, "7": U},
    "5": {"2": D, "4": L, "6": R, "8": U},
    "6": {"3": D, "5": L, "9": U},
    "7": {"4": D, "8": R},
    "8": {"5": D, "7": L, "9": R},
    "9": {"6": D, "8": L},
}
DIR = {
    A: {U: L, R: D},
    U: {A: R, D: D},
    L: {D: R},
    D: {U: U, L: L, R: R},
    R: {A: U, D: L},
}


@aoc_timer
def get_input(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


@cache
def get_paths(start: str, end: str, numeric: bool = False) -> tuple[str]:
    graph = NUM if numeric else DIR
    cost = defaultdict(lambda: math.inf, {start: 0})
    Q = []
    paths = []
    heapq.heappush(Q, (0, start, ""))
    while Q:
        cur_cost, pos, path = heapq.heappop(Q)
        if pos == end:
            paths.append(path + A)
        for new_pos, d in graph[pos].items():
            new_path = path + d
            new_cost = cur_cost + 1
            if new_cost <= cost[new_pos]:
                cost[new_pos] = new_cost
                heapq.heappush(Q, (new_cost, new_pos, new_path))
    return tuple(paths)


@cache
def seq(code: str, robots: int, path: str = None) -> int:
    numeric = path is None
    path = A + (path or code)
    result = 0
    for a, b in it.pairwise(path):
        paths = get_paths(a, b, numeric)
        if robots == 0:
            result += min(len(path) for path in paths)
        else:
            result += min(seq(code, robots - 1, path) for path in paths)
    return result


@aoc_timer
def solve(data: list[str], robots: int = 2) -> int:
    return sum(int(code[:-1]) * seq(code, robots) for code in data)


def main() -> None:
    print("AoC 2024\nDay 21")
    data = get_input("input.txt")
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, robots=25))


if __name__ == "__main__":
    main()
