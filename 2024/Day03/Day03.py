# %% Day 03
from helper import aoc_timer
import re


@aoc_timer
def get_input(path: str) -> str:
    with open(path) as f:
        return f.read()


@aoc_timer
def solve(data: str) -> tuple[int, int]:
    p1, p2, enabled = 0, 0, True
    for m in re.finditer(r"mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))", data):
        a, b, do, dont = m.groups()
        if a and b:
            n = int(a) * int(b)
            p1 += n
            p2 += enabled * n
        elif dont:
            enabled = False
        elif do:
            enabled = True
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 03")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
