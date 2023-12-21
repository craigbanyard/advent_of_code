# %% Day 16
from helper import aoc_timer
from collections import deque
import itertools as it


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


def render(energised: set[tuple[int]], R: int, C: int) -> str:
    '''Return a string representation of the energised tiles.'''
    result = ''
    for r in range(R):
        for c in range(C):
            if (r, c) in energised:
                result += '#'
            else:
                result += '.'
        result += '\n'
    return result


def configure(G: list[str], R: int, C: int, start: tuple[int]) -> int:
    '''
    Return the number of energised tiles resulting from the supplied
    configuration (starting position and direction).
    '''
    visited = set()
    Q = deque([start])
    while Q:
        r, c, dr, dc = Q.popleft()
        if not (0 <= r < R and 0 <= c < C):
            continue
        if (r, c, dr, dc) in visited:
            continue
        visited.add((r, c, dr, dc))
        if G[r][c] == '-' and dr != 0:
            for dc in (1, -1):
                Q.append((r, c + dc, 0, dc))
        elif G[r][c] == '|' and dc != 0:
            for dr in (1, -1):
                Q.append((r + dr, c, dr, 0))
        elif G[r][c] == '\\':
            Q.append((r + dc, c + dr, dc, dr))
        elif G[r][c] == '/':
            Q.append((r - dc, c - dr, -dc, -dr))
        else:
            Q.append((r + dr, c + dc, dr, dc))
    return len(set((r, c) for r, c, *_ in visited))


@aoc_timer
def solve(data: list[str]) -> tuple[int]:
    R = len(data)
    C = len(data[0])
    args = (data, R, C)
    p1 = p2 = configure(*args, (0, 0, 0, 1))
    for r, c in it.product(range(R), (0, C - 1)):
        dc = 1 if c == 0 else -1
        p2 = max(p2, configure(*args, (r, c, 0, dc)))
    for r, c in it.product((0, R - 1), range(C)):
        dr = 1 if r == 0 else -1
        p2 = max(p2, configure(*args, (r, c, dr, 0)))
    return p1, p2


def main() -> None:
    print("AoC 2023\nDay 16")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
