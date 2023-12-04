# %% Day 04
from helper import aoc_timer
from collections import Counter
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[tuple[set[str]]]:
    for line in open(path).read().splitlines():
        _, nums = line.split(': ')
        a, b = nums.split(' | ')
        yield set(a.split()), set(b.split())


@aoc_timer
def solve(data: Iterator[tuple[set[str]]]) -> tuple[int]:
    p1 = 0
    cards = Counter()
    for c, (a, b) in enumerate(data):
        cards[c] += 1
        if (w := len(a & b)):
            p1 += 2 ** (w - 1)
            for dc in range(w):
                cards[c + dc + 1] += cards[c]
    return p1, cards.total()


def main() -> None:
    print("AoC 2023\nDay 04")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
