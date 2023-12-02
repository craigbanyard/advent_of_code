# %% Day 02
from helper import aoc_timer
from collections import defaultdict
from math import prod
import re
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[str]:
    yield from open(path).read().splitlines()


@aoc_timer
def solve(data: Iterator[str]) -> tuple[int]:
    rgb = [
        r'(?P<red>\d+) red',
        r'(?P<green>\d+) green',
        r'(?P<blue>\d+) blue'

    ]
    pattern = re.compile('|'.join(rgb))
    p1, p2 = 0, 0
    config = {
        'red' : 12,
        'green': 13,
        'blue': 14
    }
    for id, game in enumerate(data, start=1):
        req = defaultdict(int)
        for m in re.finditer(pattern, game):
            for c in config.keys():
                if m.group(c) is None:
                    continue
                req[c] = max(req[c], int(m.group(c)))
        if all(v <= config[k] for k, v in req.items()):
            p1 += id
        p2 += prod(req.values())
    return p1, p2


def main() -> None:
    print("AoC 2023\nDay 02")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
