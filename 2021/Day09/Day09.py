from helper import aoc_timer
from collections import deque
import itertools as it
from math import prod
import matplotlib.pyplot as plt
import numpy as np


@aoc_timer
def get_input(path):
    G = []
    for line in open(path).read().splitlines():
        G.append([*map(int, [*line])])
    return G


@aoc_timer
def Day09(grid, **kwargs):

    D = [
        (-1, 0),    # Up
        (0, 1),     # Right
        (1, 0),     # Down
        (0, -1)     # Left
    ]

    R, C = len(grid), len(grid[0])

    def valid(r, c):
        '''Determine whether (r, c) lies in the grid.'''
        return 0 <= r < R and 0 <= c < C

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

    def visualise(grid, **kwargs):
        '''Plot a heightmap from the grid.'''
        if not kwargs.get('vis', False):
            return None
        G = np.array(grid, dtype=int)
        X, Y = np.meshgrid(np.arange(C), np.arange(R))
        Z = G[Y[::-1], X]
        cmap = kwargs.get('cmap', 'ocean')
        fig = plt.figure(figsize=kwargs.get('figsize', (10, 10)))
        match kwargs.get('proj', 'image'):
            case 'image':
                ax = fig.add_subplot()
                plt.imshow(Z, extent=(0, C, 0, R), origin='lower', cmap=cmap)
            case '2d':
                ax = fig.add_subplot()
                plt.contourf(X, Y, Z, 10, cmap=cmap)
            case '3d':
                ax = plt.axes(projection='3d')
                ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                                cmap=cmap, edgecolor='none')
            case _:
                return None
        ax.set_axis_off()
        plt.show()

    lows = deque()
    basins = deque()
    for r, c in it.product(range(R), range(C)):
        if (n := grid[r][c]) == 9:
            continue
        m = min([grid[r + dr][c + dc] for dr, dc in D
                 if valid(r + dr, c + dc)])
        if n < m:
            lows.append(n + 1)
            basins.append(bfs(grid, r, c))

    p1 = sum(lows)
    p2 = prod(sorted(basins)[-3:])

    visualise(grid, **kwargs)

    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 09")
    data = get_input('input.txt')
    p1, p2 = Day09(data, vis=True, proj='image')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
