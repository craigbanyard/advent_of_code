# %% Day 13
from helper import aoc_timer
import re

type Data = list[list[int]]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        return [list(map(int, re.findall(r"\d+", c))) for c in f.read().split("\n\n")]


@aoc_timer
def solve(data: Data, units: int = 0) -> int:
    """
    A*ax + B*bx = tx
    A*ay + B*by = ty

    A = (tx*by - bx*ty)/(ax*by - bx*ay)
    B = (tx*ay - ax*ty)/(bx*ay - ax*by)
    """
    ans = 0
    for ax, ay, bx, by, tx, ty in data:
        tx += units
        ty += units
        a = (tx * by - bx * ty) / (ax * by - bx * ay)
        b = (tx * ay - ax * ty) / (bx * ay - ax * by)
        if a == int(a) and b == int(b):
            ans += int(3 * a + b)
    return ans


def main() -> None:
    print("AoC 2024\nDay 13")
    data = get_input("input.txt")
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, units=10000000000000))


if __name__ == "__main__":
    main()
