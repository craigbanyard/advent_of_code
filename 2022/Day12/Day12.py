from helper import aoc_timer, Grid
from string import ascii_lowercase as letters
import itertools as it
from typing import Iterator


class Heightmap(Grid):
    E = {v: k for k, v in enumerate(letters)}
    E['S'] = E['a']
    E['E'] = E['z']

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def valid(self, node: tuple[int, int]) -> bool:
        '''
        Overridden method for 2022 Day 12:
        All nodes within the grid are traversable.
        '''
        r, c = node
        return 0 <= r < self._R and 0 <= c < self._C

    def neighbours(self, node: tuple[int, int]) -> tuple[int, int]:
        '''
        Overridden method for 2022 Day 12:
        Can only move to a position at most one elevation
        higher than the current position.
        '''
        r, c = node
        e = self.G[r][c]
        for dr, dc in self.D:
            if self.valid(((rr := r + dr), (cc := c + dc))):
                ee = self.G[rr][cc]
                if self.E[ee] - self.E[e] <= 1:
                    yield (rr, cc)

    def find(self, letter: str) -> Iterator[tuple[int, int]]:
        '''
        New method for 2022 Day 12:
        Return a generator of nodes with the value letter.
        '''
        for r, c in it.product(range(self._R), range(self._C)):
            if self.G[r][c] == letter:
                yield (r, c)


@aoc_timer
def get_input(path: str) -> list[list[str]]:
    return [[*line] for line in open(path).read().splitlines()]


def shortest_path(G: Heightmap, start: tuple[int, int],
                  end: tuple[int, int]) -> int:
    '''
    Return the shortest path from start to end using
    breadth-first search (BFS) on the grid, G.
    There is no need for Djikstra (or A*) here since
    the movement cost is constant.
    '''
    _, cost = G.bfs(start, end)
    return cost[end]


@aoc_timer
def solve(data: list[list[str]]) -> tuple[int, int]:
    G = Heightmap(G=data)
    start = next(G.find('S'), (0, 0))
    end = next(G.find('E'), (G._R, G._C))
    p1 = shortest_path(G, start, end)
    p2 = p1
    for start in G.find('a'):
        # Brute force. If we override the pathing algorithm
        # to account for already computed paths, we can do
        # this part much more efficiently.
        p2 = min(p2, shortest_path(G, start, end))
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 12")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
