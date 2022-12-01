from helper import aoc_timer, Colours, Grid
from collections import defaultdict
import heapq
import math


@aoc_timer
def get_input(path):
    with open(path) as f:
        return int(f.read())


@aoc_timer
def Day13(data, start, target=None, max_steps=None, astar=False, vis=False):

    D = [
        (0, -1),    # Up
        (0, 1),     # Down
        (-1, 0),    # Left
        (1, 0)      # Right
    ]

    def valid(x, y):
        '''
        Return True if (x, y) is an open space.
        Return False if (x, y) is a wall.
        '''
        if x < 0 or y < 0:
            return False
        val = data + (x*x + 3*x + 2*x*y + y + y*y)
        return bin(val).count('1') % 2 == 0

    def neighbours(pos):
        '''
        Return a generator of valid neighbours (open spaces)
        of pos.
        '''
        x, y = pos
        for dx, dy in D:
            if valid((xx := x + dx), (yy := y + dy)):
                yield (xx, yy)

    def h(a, b):
        '''A* heuristic: Manhattan distance between points a and b.'''
        if astar and b is not None:
            return sum(abs(p - q) for p, q in zip(a, b))
        return 0

    def construct_path(paths, start, end):
        '''
        Return a set of coordinates (x, y) that comprise the
        optimal path from start to end.
        If end is None, return the set of all visited points.

        '''
        if target is None:
            return set(paths.keys()) | {start}
        if end not in paths:
            return None
        c = end
        path = set([c])
        while c in paths:
            c = paths[c]
            path.add(c)
            if c == start:
                return path
        return None

    def visualise(path):
        '''
        Return a string representation of the path traced
        by the set of coordinates passed as the argument.
        The path is highlighted in bold and cyan.
        '''
        min_x, min_y = [min(c) - 1 for c in zip(*path)]
        max_x, max_y = [max(c) + 1 for c in zip(*path)]
        maze = ''
        highlight = Colours.BOLD + Colours.fg.CYAN
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in path:
                    maze += f'{highlight}O{Colours.ENDC}'
                elif valid(x, y):
                    maze += '.'
                else:
                    maze += '#'
            maze += '\n'
        return maze

    cost = defaultdict(lambda: math.inf, {start: 0})
    prev = {}
    heapq.heappush(Q := [], (0, start))

    # Djikstra (or A* if heuristic is used)
    while Q:
        _, pos = heapq.heappop(Q)
        if pos == target:
            break
        for new_pos in neighbours(pos):
            new_cost = cost[pos] + 1
            if new_cost < cost[new_pos]:
                cost[new_pos] = new_cost
                prev[new_pos] = pos
                priority = new_cost + h(new_pos, target)
                heapq.heappush(Q, (priority, new_pos))
        if cost[new_pos] == max_steps:
            break
    if vis:
        path = construct_path(prev, start, target)
        print(visualise(path))
    if target is None:
        return len(cost)
    return cost[target]


# %% Solution using Grid helper class
class D13(Grid):
    def __init__(self, data, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = data

    def valid(self, node):
        '''
        Return True if (x, y) is an open space.
        Return False if (x, y) is a wall.
        '''
        y, x = node
        if x < 0 or y < 0:
            return False
        val = self.data + (x*x + 3*x + 2*x*y + y + y*y)
        return bin(val).count('1') % 2 == 0


def Day13_Grid(data, start, end):
    grid = D13(data)
    _, p1 = grid.djikstra(start, end)
    _, p2 = grid.djikstra(start, end=None, max_cost=50)
    return p1[end], len(p2)


# %% Output
def main():
    print("AoC 2016\nDay 13")
    data = get_input('input.txt')
    start = (1, 1)
    p1 = Day13(data, start, target=(31, 39), astar=True, vis=True)
    print("Part 1:", p1, '\n')
    p2 = Day13(data, start, max_steps=50, vis=True)
    print("Part 2:", p2)
    p1_grid, p2_grid = Day13_Grid(data, start, end=(39, 31))
    assert p1 == p1_grid
    assert p2 == p2_grid


if __name__ == '__main__':
    main()
