from helper import aoc_timer


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


@aoc_timer
def solve(data: list[str], part: int) -> int:
    scores = {
        'A X': {1: 1 + 3, 2: 3 + 0},
        'A Y': {1: 2 + 6, 2: 1 + 3},
        'A Z': {1: 3 + 0, 2: 2 + 6},
        'B X': {1: 1 + 0, 2: 1 + 0},
        'B Y': {1: 2 + 3, 2: 2 + 3},
        'B Z': {1: 3 + 6, 2: 3 + 6},
        'C X': {1: 1 + 6, 2: 2 + 0},
        'C Y': {1: 2 + 0, 2: 3 + 3},
        'C Z': {1: 3 + 3, 2: 1 + 6}
    }
    return sum(scores[hand][part] for hand in data)


# %% Output
def main() -> None:
    print("AoC 2022\nDay 02")
    data = get_input('input.txt')
    print("Part 1:", solve(data, part=1))
    print("Part 2:", solve(data, part=2))


if __name__ == '__main__':
    main()
