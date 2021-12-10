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
def Day09(data):
    
    D = [
        (-1, 0),    # Up
        (1, 0),     # Down
        (0, -1),    # Left
        (0, 1)      # Right
    ]

    R, C = len(data), len(data[0])

    lows = {}

    for r, _ in enumerate(data):
        for c, n in enumerate(data[r]):
            if n == 9:
                continue
            m = np.inf
            for dr, dc in D:
                if (rr := r + dr) not in range(R) or (cc := c + dc) not in range(C):
                    continue
                m = min(m, data[rr][cc])
            if n < m:
                lows[(r, c)] = n + 1

    p1 = sum(lows.values())

    # Part 2
    basins = {k: set() for k in lows}
    Q = deque()
    visited = set()
    for (r, c) in basins:
        low = (r, c)
        Q.append((r, c))
        while Q:
            r, c = Q.popleft()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in D:
                if (rr := r + dr) not in range(R) or (cc := c + dc) not in range(C):
                    continue
                if data[rr][cc] != 9:
                    Q.append((rr, cc))
                    basins[low].add((rr, cc))

    p2 = 1
    for k in sorted(basins, key=lambda k: len(basins[k]), reverse=True)[:3]:
        p2 *= len(basins[k])

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
