# %% Day 11
from helper import aoc_timer
import itertools as it


@aoc_timer
def get_input(path: str) -> list[tuple[int]]:
    img = []
    for r, line in enumerate(open(path).read().splitlines()):
        for c, ch in enumerate(line):
            if ch == '#':
                img.append((r, c))
    return img


def expand(img: list[tuple[int]], expansion_factor: int) -> list[tuple[int]]:
    '''
    Returns an expanded version of the supplied universe image,
    where each empty row and column is expanded by a factor.
    '''
    for axis in (0, 1):
        prev, e = 0, 0
        img = list(sorted(img, key=lambda x: x[axis]))
        for idx, point in enumerate(img):
            if (d := point[axis] - prev) > 1:
                e += (expansion_factor - 1) * (d - 1)
            r, c = point
            if axis == 0:
                dr, dc = e, 0
            elif axis == 1:
                dr, dc = 0, e
            img[idx] = (r + dr, c + dc)
            prev = point[axis]
    return img


def manhattan(points: tuple[tuple[int]]) -> int:
    '''Returns the Manhattan distance between two points.'''
    return sum(abs(p - q) for p, q in zip(*points))


@aoc_timer
def solve(data: list[tuple[int]], expansion_factor: int = 2) -> int:
    img = expand(data, expansion_factor)
    return sum(map(manhattan, it.combinations(img, 2)))


def main() -> None:
    print("AoC 2023\nDay 11")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, expansion_factor=1000000))


if __name__ == '__main__':
    main()
