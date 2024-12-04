# %% Day 04
from helper import aoc_timer
import itertools as it
import numpy as np


@aoc_timer
def get_input(path: str) -> np.ndarray:
    with open(path) as f:
        return np.array([[ch for ch in line] for line in f.read().splitlines()])


def find(arr: np.ndarray, word: str) -> bool:
    return "".join(arr) == word


class Solver:
    def __init__(self, data: np.ndarray, word: str, part2: bool) -> None:
        self.data = data
        self.word = word
        self.part2 = part2
        self.R, self.C = data.shape
        self.S = {w[0]: w[1:] for w in (word, word[::-1])}

    def find_xmas(self) -> int:
        ans = 0
        for r, c in it.product(range(self.R), range(self.C)):
            if (suffix := self.S.get(self.data[r, c])) is None:
                continue
            r0, r1, c0, c1 = r + 1, r + 4, c + 1, c + 4
            if c1 <= self.C:
                ans += find(self.data[r, c0:c1], suffix)
            if r1 <= self.R:
                ans += find(self.data[r0:r1, c], suffix)
            if r1 <= self.R and c1 <= self.C:
                ans += find(self.data[range(r0, r1), range(c0, c1)], suffix)
            if r1 <= self.R and c >= 3:
                ans += find(self.data[range(r0, r1), range(c - 1, c - 4, -1)], suffix)
        return ans

    def find_x_mas(self) -> int:
        ans = 0
        for r, c in it.product(range(self.R - 2), range(self.C - 2)):
            if (dr_suffix := self.S.get(self.data[r, c])) is None:
                continue
            if (dl_suffix := self.S.get(self.data[r, c + 2])) is None:
                continue
            r0, r1, c0 = r + 1, r + 3, c + 1
            ans += (
                find(self.data[range(r0, r1), range(c0, c + 3)], dr_suffix) and
                find(self.data[range(r0, r1), range(c0, c - 1, - 1)], dl_suffix)
            )
        return ans

    def solve(self) -> int:
        if self.part2:
            return self.find_x_mas()
        return self.find_xmas()


@aoc_timer
def solve(data: np.ndarray, word: str, part2: bool = False) -> int:
    solver = Solver(data, word, part2)
    return solver.solve()


def main() -> None:
    print("AoC 2024\nDay 04")
    data = get_input("input.txt")
    print("Part 1:", solve(data, word="XMAS"))
    print("Part 2:", solve(data, word="MAS", part2=True))


if __name__ == "__main__":
    main()
