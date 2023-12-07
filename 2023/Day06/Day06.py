# %% Day 06
from helper import aoc_timer
import re
from typing import Iterator


@aoc_timer
def get_input(path: str, spaces: bool = True) -> Iterator[tuple[int]]:
    nums = [re.findall(r'\d+', line.replace(' ', ' ' * spaces))
            for line in open(path).read().splitlines()]
    return zip(*[map(int, line) for line in nums])


@aoc_timer
def solve(data: Iterator[tuple[int]]) -> int:
    ans = 1
    for t, r in data:
        wins = 0
        for dt in range(1, t // 2 + 1):
            if dt * (t - dt) > r:
                wins += 2
        if t % 2 == 0:
            wins -= 1
        ans *= wins
    return ans


def main() -> None:
    print("AoC 2023\nDay 06")
    data = get_input('input.txt', spaces=True)
    print("Part 1:", solve(data))
    data = get_input('input.txt', spaces=False)
    print("Part 2:", solve(data))


if __name__ == '__main__':
    main()
