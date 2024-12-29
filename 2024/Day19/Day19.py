# %% Day 19
from helper import aoc_timer
from functools import cache

type Data = tuple[list[str], list[str]]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        towels, designs = f.read().split("\n\n")
    return towels.split(", "), designs.splitlines()


@aoc_timer
def solve(data: Data) -> int:
    towels, designs = data

    @cache
    def make(design: str) -> int:
        if not design:
            return 1
        result = 0
        for t in towels:
            if design.startswith(t):
                result += make(design.removeprefix(t))
        return result

    p1 = p2 = 0
    for design in designs:
        ways = make(design)
        p1 += ways > 0
        p2 += ways
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 19")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
