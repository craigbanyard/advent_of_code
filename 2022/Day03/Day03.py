from helper import aoc_timer
from string import ascii_letters as letters
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[str]:
    for line in open(path).read().splitlines():
        yield line


@aoc_timer
def solve(data: Iterator[str]) -> tuple[int, int]:
    priority = {k: v for v, k in enumerate(letters, start=1)}
    p1, p2 = 0, 0
    for idx, rucksack in enumerate(data):
        # Part 1
        m = len(rucksack)//2
        a, b = rucksack[:m], rucksack[m:]
        common, = set(a) & set(b)
        p1 += priority[common]
        # Part 2
        if idx % 3 == 0:
            group = set(rucksack)
        else:
            group &= set(rucksack)
        if idx % 3 == 2:
            badge, = group
            p2 += priority[badge]
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 03")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
