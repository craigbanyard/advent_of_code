from helper import aoc_timer
from collections import deque
import numpy as np


@aoc_timer
def get_input(path):
    G = []
    for line in open(path).read().splitlines():
        G.append([*line])
    return np.array(G, dtype=int)


@aoc_timer
def Day09(grid):

    D = [
        (-1, 0),    # Up
        (1, 0),     # Down
        (0, -1),    # Left
        (0, 1)      # Right
    ]

    R, C = len(grid), len(grid[0])

    def valid(r, c):
        '''Determine whether (r, c) lies in the grid.'''
        return r in range(R) and c in range(C)

    def bfs(grid, r, c):
        '''
        Perform BFS on a grid from starting point, (r, c).
        Returns basin size, the length of the visited set.
        '''
        visited = set()
        Q = deque([(r, c)])
        while Q:
            r, c = Q.popleft()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in D:
                if valid(rr := r + dr, cc := c + dc) and grid[rr][cc] != 9:
                    Q.append((rr, cc))
        return len(visited)

    lows = {}
    basins = {}
    for r, _ in enumerate(grid):
        for c, n in enumerate(grid[r]):
            if n == 9:
                continue
            m = min([grid[r + dr][c + dc] for dr, dc in D
                     if valid(r + dr, c + dc)])
            if n < m:
                lows[(r, c)] = n + 1
                basins[(r, c)] = bfs(grid, r, c)

    p1 = sum(lows.values())

    p2 = 1
    for k in sorted(basins, key=basins.get, reverse=True)[:3]:
        p2 *= basins[k]

    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 09")
    data = get_input('input.txt')
    p1, p2 = Day09(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
