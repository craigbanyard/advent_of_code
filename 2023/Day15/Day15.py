# %% Day 15
from helper import aoc_timer
from collections import defaultdict
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[str]:
    yield from open(path).read().split(',')


@aoc_timer
def solve(data: Iterator[str]) -> tuple[int]:
    boxes = defaultdict(list)
    p1, p2 = 0, 0
    for step in data:
        n = 0
        for c in step:
            if c == '-':
                for label, foc in boxes[n]:
                    if label == step[:-1]:
                        boxes[n].remove((label, foc))
                        break
            elif c == '=':
                label, foc = step.split('=')
                for idx, (existing, _) in enumerate(boxes[n]):
                    if existing == label:
                        boxes[n][idx] = (label, int(foc))
                        break
                else:
                    boxes[n].append((label, int(foc)))
            n = (n + ord(c)) * 17 % 256
        p1 += n
    for idx, box in boxes.items():
        for slot, (_, foc) in enumerate(box, start=1):
            p2 += (idx + 1) * (slot * foc)
    return p1, p2


def main() -> None:
    print("AoC 2023\nDay 15")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
