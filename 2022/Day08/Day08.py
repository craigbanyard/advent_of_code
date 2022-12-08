from helper import aoc_timer
from math import prod


@aoc_timer
def get_input(path: str) -> list[list[int]]:
    return [[int(c) for c in r]
            for r in open(path).read().splitlines()]


@aoc_timer
def solve(data: list[list[int]]) -> tuple[int, int]:
    R = len(data)
    C = len(data[0])
    p1, p2 = 0, 0
    for r in range(R):
        for c in range(C):
            vis = [True] * 4
            score = [0] * 4
            if r > 0 and c > 0:
                for rr in range(r - 1, -1, -1):
                    score[0] += 1
                    if data[r][c] <= data[rr][c]:
                        vis[0] = False
                        break
                for rr in range(r + 1, R):
                    score[1] += 1
                    if data[r][c] <= data[rr][c]:
                        vis[1] = False
                        break
                for cc in range(c - 1, -1, -1):
                    score[2] += 1
                    if data[r][c] <= data[r][cc]:
                        vis[2] = False
                        break
                for cc in range(c + 1, C):
                    score[3] += 1
                    if data[r][c] <= data[r][cc]:
                        vis[3] = False
                        break
            if any(vis):
                p1 += 1
            p2 = max(p2, prod(score))
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
