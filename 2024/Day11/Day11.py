# %% Day 11
from helper import aoc_timer, num_digits
from collections import Counter
import math


@aoc_timer
def get_input(path: str) -> list[int]:
    with open(path) as f:
        return [*map(int, f.read().strip().split())]


@aoc_timer
def solve(data: list[int], blinks: int = 25) -> int:
    stones = Counter(data)
    for _ in range(blinks):
        for stone, n in stones.copy().items():
            if stone == 0:
                stones[1] += n
            elif (d := num_digits(stone)) % 2 == 0:
                a, b = divmod(stone, math.pow(10, d // 2))
                stones[a] += n
                stones[b] += n
            else:
                stones[stone * 2024] += n
            stones[stone] -= n
    return stones.total()


def main() -> None:
    print("AoC 2024\nDay 11")
    data = get_input("input.txt")
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, blinks=75))


if __name__ == "__main__":
    main()
