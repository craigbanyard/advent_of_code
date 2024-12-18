# %% Day 14
from helper import aoc_timer
from io import StringIO
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
from operator import gt, lt
import re

type Data = tuple[np.ndarray, np.ndarray]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        a = np.array(re.findall(r"-?\d+", f.read()), dtype="int64").reshape((-1, 4))
    return a[:, 0] + a[:, 1] * 1j, a[:, 2] + a[:, 3] * 1j


class Robots:
    def __init__(self, data: Data, r: int, c: int, vis: str = "") -> None:
        self.p, self.v = data
        self.R = r
        self.C = c
        self.vis = vis
        self.r = r // 2
        self.c = c // 2
        self.t = 0

    def __repr__(self) -> str:
        out = StringIO()
        out.write(f"t={self.t}")
        for r, c in it.product(range(self.R), range(self.C)):
            if c == 0:
                out.write("\n")
            if complex(c, r) in self.p:
                out.write("#")
            else:
                out.write(".")
        return out.getvalue()

    def move(self, t: int = 1) -> None:
        self.p += t * self.v
        self.p.real %= self.C
        self.p.imag %= self.R
        self.t += t

    def score(self) -> int:
        qs = [
            self.p[(f(self.p.real, self.c) & g(self.p.imag, self.r))]
            for f, g in it.product([lt, gt], repeat=2)
        ]
        return np.prod([q.size for q in qs])

    def plot(self) -> None:
        _, ax = plt.subplots()
        ax.set_axis_off()
        ax.scatter(self.p.real, -self.p.imag, s=8, c=("forestgreen", 0.5))

    def view(self) -> None:
        if self.vis == "ascii":
            print(self)
        elif self.vis == "plot":
            self.plot()


@aoc_timer
def solve(
    data: Data,
    r: int = 103,
    c: int = 101,
    t: int = 100,
    max_t: int = 10000,
    vis: str = "",
) -> tuple[int, int]:
    robots = Robots(data, r, c, vis)
    robots.move(t)
    p1 = robots.score()
    p2 = t
    min_score = p1
    for _ in it.count(robots.t):
        robots.move()
        if (score := robots.score()) < min_score:
            p2 = robots.t
            min_score = score
            robots.view()
        if robots.t > max_t:
            break
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 14")
    data = get_input("input.txt")
    p1, p2 = solve(data, vis="plot")
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
