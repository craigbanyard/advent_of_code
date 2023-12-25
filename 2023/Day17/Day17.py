# %% Day 17
from helper import aoc_timer, Colours, Grid
from collections import defaultdict
import heapq
import math
from typing import Iterator


class Map(Grid):

    D = {
        (-1, 0): '^',
        (1, 0): 'v',
        (0, -1): '<',
        (0, 1): '>'
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.minspeed = kwargs.get('minspeed', 0)
        self.maxspeed = kwargs.get('maxspeed', math.inf)

    @property
    def shape(self) -> tuple[int]:
        '''Return the shape of the grid.'''
        return (self._R - 1, self._C - 1)

    def valid(self, node) -> bool:
        '''Determine whether a given node is traversable.'''
        r, c = node
        return 0 <= r < self._R and 0 <= c < self._C

    def neighbours(self, head, speed) -> Iterator[tuple]:
        '''Yield each new valid heading and speed.'''
        if speed < self.maxspeed:
            yield head, speed + 1
        if speed >= self.minspeed or speed == 0:
            match head:
                case (_, 0):
                    yield (0, 1), 1
                    yield (0, -1), 1
                case (0, _):
                    yield (1, 0), 1
                    yield (-1, 0), 1

    def cost(self, node) -> int:
        '''Cost to move to node.'''
        r, c = node
        return self.G[r][c]

    def djikstra(self, start, end, h=lambda a, b: 0,
                 max_cost=math.inf) -> tuple[dict, dict]:
        '''Perform Djikstra's algorithm on the grid.'''
        visited = {}
        cost = defaultdict(lambda: math.inf, {start: 0})
        Q = []
        heapq.heappush(Q, (0, start))
        while Q:
            _, state = heapq.heappop(Q)
            pos, head, speed = state
            if self._traversal_complete(state, cost, end, max_cost):
                break
            for (dr, dc), new_speed in self.neighbours(head, speed):
                r, c = pos
                new_pos = (r + dr, c + dc)
                if not self.valid(new_pos):
                    continue
                new_state = (new_pos, (dr, dc), new_speed)
                new_cost = cost[state] + self.cost(new_pos)
                if new_cost < cost[new_state]:
                    cost[new_state] = new_cost
                    visited[new_state] = state
                    priority = new_cost + h(new_pos, end)
                    heapq.heappush(Q, (priority, new_state))
        return visited, cost

    def construct_path(self, start, end, visited) -> dict:
        '''
        Return a dictionary of (r, c): (heading, speed) that comprises the path
        from start to end implied by the visited dictionary.
        If end is None, return the dictionary of visited nodes including start.
        '''
        if end is None:
            return {k: v for k, v in (visited.keys() | {start})}
        if end not in visited:
            return {}
        p, h, s = end
        path = {p: (h, s)}
        while (p, h, s) in visited:
            (p, h, s) = visited[(p, h, s)]
            path[p] = (h, s)
            if (p, h, s) == start:
                return path
        return {}

    def visualise_path(self, path) -> str | None:
        '''
        Return a string representation of the path provided as the argument.
        '''
        if not path:
            return None
        min_r, min_c = 0, 0
        max_r, max_c = self._R, self._C
        grid = ''
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                v = str(self.G[r][c])
                if (r, c) in path:
                    h, _ = path[(r, c)]
                    v = self.D.get(h, v)
                    grid += Colours.BOLD + Colours.fg.CYAN + v + Colours.ENDC
                else:
                    grid += v
            grid += '\n'
        return grid


@aoc_timer
def get_input(path: str) -> list[list[int]]:
    return [[*map(int, line)] for line in open(path).read().splitlines()]


@aoc_timer
def solve(data: list[list[int]], minspeed: int = 0, maxspeed: int = 3,
          vis: bool = False) -> int:
    M = Map(G=data, minspeed=minspeed, maxspeed=maxspeed)
    start = ((0, 0), (0, 0), 0)
    visited, cost = M.djikstra(start=start, end=M.shape)
    ends = {(p, h, s): v for (p, h, s), v in cost.items()
            if p == M.shape and s >= minspeed}
    end = min(ends, key=ends.get)
    if vis:
        print(M.visualise_path(M.construct_path(start, end, visited)))
    return cost[end]


def main() -> None:
    print("AoC 2023\nDay 17")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, minspeed=4, maxspeed=10))


if __name__ == '__main__':
    main()
