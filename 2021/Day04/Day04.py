from helper import aoc_timer
from collections import defaultdict
import numpy as np


@aoc_timer
def get_input(path: str) -> tuple[np.ndarray, dict[np.ndarray]]:
    draw = None
    boards = defaultdict(list)
    idx = -1
    for line in open(path).read().splitlines():
        if draw is None:
            draw = np.array(line.split(','), dtype=int)
            continue
        if not line:
            idx += 1
            continue
        boards[idx].append(np.array(line.split(), dtype=int))
    boards = {k: np.stack(v, axis=0) for k, v in boards.items()}
    return draw, boards


def score(n: int, k: int, board: np.ndarray, marks: dict[np.ndarray]) -> int:
    """
    Return the score of the given bingo board.
    This is calculated as the sum of the unmarked numbers
    multiplied by the last number called.
    """
    return n * np.sum(np.invert(marks[k]) * board)


@aoc_timer
def Day04(data: tuple[np.ndarray, dict[np.ndarray]]):
    draw, boards = data
    marks = {k: False for k in boards.keys()}
    play = set(boards.keys())
    for n in draw:
        boards = {k: boards[k] for k in play}
        for k, board in boards.items():
            marks[k] ^= board == n
            r = np.all(marks[k], axis=0)
            c = np.all(marks[k], axis=1)
            if np.any(r ^ c):
                yield score(n, k, board, marks)
                play.remove(k)
            if not play:
                return score(n, k, board, marks)


# %% Output
def main():
    print("AoC 2021\nDay 04")
    data = get_input('input.txt')
    p1, *_, p2 = Day04(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
