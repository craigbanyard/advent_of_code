# %% Day 08
from helper import aoc_timer
from collections import defaultdict
import itertools as it


type Data = tuple[dict[str, list[complex]], tuple[int, int]]


@aoc_timer
def get_input(path: str) -> Data:
    A = defaultdict(list)
    with open(path) as f:
        for r, line in enumerate(f.read().splitlines()):
            for c, ch in enumerate(line):
                if ch == ".":
                    continue
                A[ch].append(complex(c, r))
    return A, (r + 1, c + 1)


class Antinodes(set):
    """Only supports creation of empty set objects."""
    def __init__(self, bounds: tuple[int, int]) -> None:
        self.R, self.C = bounds

    def create(self, element: complex, distance: complex | None = None) -> None:
        while 0 <= element.imag < self.R and 0 <= element.real < self.C:
            self.add(element)
            if distance is None:
                return
            element += distance


@aoc_timer
def solve(data: Data) -> tuple[int, int]:
    A, bounds = data
    p1, p2 = Antinodes(bounds), Antinodes(bounds)
    for _, antennas in A.items():
        for a, b in it.combinations(antennas, 2):
            for p, q in zip([a, b], [a - b, b - a]):
                p1.create(p + q)
                p2.create(p, q)
    return len(p1), len(p2)


def main() -> None:
    print("AoC 2024\nDay 08")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
