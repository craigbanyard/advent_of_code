from helper import aoc_timer
import itertools as it
import math
from typing import Iterator


@aoc_timer
def get_input(path: str) -> list[list[int]]:
    return [[int(c) for c in r]
            for r in open(path).read().splitlines()]


@aoc_timer
def solve(data: list[list[int]]) -> tuple[int, int]:
    R = len(data)
    C = len(data[0])

    def directions(r: int, c: int) -> Iterator[range]:
        '''
        Return generators for trees in each direction
        starting from (r, c).
        '''
        yield range(r-1, -1, -1)    # Up
        yield range(r+1, R)         # Down
        yield range(c-1, -1, -1)    # Left
        yield range(c+1, C)         # Right

    p1, p2 = 0, 0
    for r, c in it.product(range(R), range(C)):
        vis = [True] * 4
        score = [0] * 4
        if r > 0 and c > 0:
            for d, rng in enumerate(directions(r, c)):
                v = d < 2
                for dr in rng:
                    score[d] += 1
                    compare = data[dr if v else r][dr if not v else c]
                    if data[r][c] <= compare:
                        vis[d] = False
                        break
        if any(vis):
            p1 += 1
        p2 = max(p2, math.prod(score))
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 08")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
