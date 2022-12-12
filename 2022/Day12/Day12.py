from helper import aoc_timer, Grid
from string import ascii_lowercase as letters


class Heightmap(Grid):
    E = {ltr: idx for idx, ltr in enumerate(letters)}
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


@aoc_timer
def get_input(path: str) -> list[list[str]]:
    return [[*line] for line in open(path).read().splitlines()]


@aoc_timer
def solve(data: list[list[str]]) -> tuple[int, int]:
    G = Heightmap(G=data)
    p1 = G.shortest_path('S', 'E', 'bfs')
    p2 = G.shortest_path('a', 'E', 'bfs')
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
