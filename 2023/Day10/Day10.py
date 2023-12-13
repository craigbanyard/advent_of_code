# %% Day 10
from helper import aoc_timer, Colours, Grid
from typing import Iterator


class Pipes(Grid):

    D = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }
    N = {
        'U': set('╔╗║'),
        'D': set('╚╝║'),
        'L': set('╔╚═'),
        'R': set('╗╝═')
    }
    P = {
        '╔': 'RD',
        '╚': 'RU',
        '╗': 'LD',
        '╝': 'LU',
        '║': 'UD',
        '═': 'LR',
        'S': 'UDLR'
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        '''String representation of the grid.'''
        out = ''
        for r in range(self._R):
            for c in range(self._C):
                out += self.G[r][c]
            out += '\n'
        return out

    def valid(self, node) -> bool:
        '''Determine whether a given node is traversable.'''
        r, c = node
        return 0 <= r < self._R and 0 <= c < self._C

    def neighbours(self, node) -> Iterator[tuple]:
        '''
        Return a generator of valid neighbours (open spaces) of the current
        node.
        '''
        r, c = node
        v = self.G[r][c]
        for d in self.P[v]:
            dr, dc = self.D[d]
            if not self.valid(((rr := r + dr), (cc := c + dc))):
                continue
            if self.G[rr][cc] in self.N[d]:
                yield (rr, cc)

    def start_tile(self, cost) -> str:
        '''Return the pipe type that matches the starting tile.'''
        p = {v: k for k, v in self.P.items()}
        d = {v: k for k, v in self.D.items()}
        (r1, c1), (r2, c2), (r3, c3), *_ = sorted(cost, key=cost.get)
        neighbours = d[(r2 - r1, c2 - c1)] + d[(r3 - r1, c3 - c1)]
        if neighbours in p:
            return p[neighbours]
        return p[neighbours[::-1]]

    def scanline(self, cost) -> set:
        '''
        Perform the scanline algorithm to determine the number of interior
        points enclosed by the path traced by the cost dictionary. Assumes the
        supplied path forms a closed loop. Returns the set of interior points.
        '''
        result = set()
        inflections = {
            '╔': '╝',
            '╚': '╗'
        }
        for r in range(self._R):
            inner = False
            last = ''
            for c in range(self._C):
                if (r, c) in cost:
                    if (v := self.G[r][c]) == 'S':
                        v = self.start_tile(cost)
                    if v == '║':
                        inner = not inner
                    elif v in inflections:
                        last = v
                    elif v in inflections.values():
                        if v == inflections[last]:
                            inner = not inner
                        last = ''
                elif inner:
                    result.add((r, c))
        return result

    def visualise_path(self, path, interior=None) -> str | None:
        '''
        Return a string representation of the path provided as the argument.
        Optionally provide a set of interior points to plot in a different
        colour from the path.
        '''
        if not path:
            return None
        if self._R * self._C > 0:
            min_r, min_c = 0, 0
            max_r, max_c = self._R, self._C
        else:
            min_r, min_c = [min(c) - 1 for c in zip(*path)]
            max_r, max_c = [max(c) + 1 for c in zip(*path)]
        grid = ''
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                v = self.G[r][c]
                if (r, c) in path:
                    if v == 'S':
                        grid += f'{Colours.fg.PINK}{v}{Colours.ENDC}'
                    else:
                        grid += f'{Colours.fg.CYAN}{v}{Colours.ENDC}'
                elif interior is not None and (r, c) in interior:
                    grid += f'{Colours.fg.YELLOW}{v}{Colours.ENDC}'
                else:
                    grid += v
            grid += '\n'
        return grid


@aoc_timer
def get_input(path: str) -> list[list[str]]:
    return [[*line.translate(str.maketrans('|-F7LJ', '║═╔╗╚╝'))]
            for line in open(path).read().splitlines()]


@aoc_timer
def solve(data: list[list[str]], vis: bool = False) -> int:
    pipes = Pipes(G=data)
    start = next(pipes.where('S'))
    _, cost = pipes.bfs(start=start, end=None)
    interior = pipes.scanline(cost)
    if vis:
        print(pipes.visualise_path(cost.keys(), interior))
    return max(cost.values()), len(interior)


def main() -> None:
    print("AoC 2023\nDay 10")
    data = get_input('input.txt')
    p1, p2 = solve(data, vis=True)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
