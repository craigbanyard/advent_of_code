# %% Day 01
from helper import aoc_timer
import re


D = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


@aoc_timer
def solve(data: list[str], sub_words: bool = False) -> int:
    ans = 0
    pattern = re.compile(rf'(?=({'|'.join(D.keys())}))')
    for line in data:
        if sub_words:
            line = re.sub(pattern, lambda k: D[k.groups()[0]], line)
        digits = re.findall(r'\d', line)
        ans += int(digits[0] + digits[-1])
    return ans


def main() -> None:
    print("AoC 2023\nDay 01")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, sub_words=True))


if __name__ == '__main__':
    main()
