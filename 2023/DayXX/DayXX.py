# %% Day XX
from helper import aoc_timer


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


@aoc_timer
def solve(data: list[str]) -> int:
    print(data)
    return 0


def main() -> None:
    print("AoC 2023\nDay XX")
    data = get_input('input.txt')
    data = get_input('sample.txt')
    print("Part 1:", solve(data))
    # print("Part 2:", solve(data))


if __name__ == '__main__':
    main()
