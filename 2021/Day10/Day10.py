from helper import aoc_timer
from collections import deque


@aoc_timer
def get_input(path):
    for line in open(path).read().splitlines():
        yield line


@aoc_timer
def Day10(data):
    p1 = 0
    scores = []
    CLOSE = {
        ')': '(',
        ']': '[',
        '}': '{',
        '>': '<'
    }
    OPEN = {v: k for k, v in CLOSE.items()}
    SYNTAX = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    AUTOCOMPLETE = {k: idx + 1 for idx, k in enumerate(SYNTAX)}

    for line in data:
        stack = deque()
        for ch in line:
            if ch in CLOSE:
                if stack.pop() != CLOSE[ch]:
                    p1 += SYNTAX[ch]
                    break
            else:
                stack.append(ch)
        else:
            # Incomplete line (i.e. didn't encounter break)
            score = 0
            while stack:
                close = OPEN[stack.pop()]
                score = 5 * score + AUTOCOMPLETE[close]
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
