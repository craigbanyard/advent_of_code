from helper import aoc_timer
from collections import deque


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        yield line


@aoc_timer
def Day10(data):
    OPEN = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    CLOSE = {v: k for k, v in OPEN.items()}
    SCORES = {
        ')': (3, 1),
        ']': (57, 2),
        '}': (1197, 3),
        '>': (25137, 4)
    }

    p1 = 0
    scores = []
    for line in data:
        stack = deque()
        for ch in line:
            if ch in OPEN:
                stack.append(ch)
            elif stack.pop() != CLOSE[ch]:
                p1 += SCORES[ch][0]
                break
        else:   # Incomplete line (i.e. didn't encounter break)
            score = 0
            while stack:
                ch = OPEN[stack.pop()]
                score = 5 * score + SCORES[ch][1]
            scores.append(score)
    p2 = sorted(scores)[len(scores) // 2]
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 10")
    data = get_input('input.txt')
    p1, p2 = Day10(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
