from helper import Colours
from collections import defaultdict, deque
import heapq
import math


class Grid:

    D = [
        (-1, 0),    # Up
        (1, 0),     # Down
        (0, -1),    # Left
        (0, 1)      # Right
    ]

    DD = [
        (-1, 1),    # Up-right
        (1, 1),     # Down-right
        (1, -1),    # Down-left
        (-1, -1)    # Up-left
    ]

    def __init__(self, **kwargs) -> None:
        self.G = kwargs.get('G', [[]])
        self._R = len(self.G)
        self._C = len(self.G[0])
        self._space = kwargs.get('space', '.')
        self._wall = kwargs.get('wall', '#')
        self.start = kwargs.get('start', (0, 0))
        self.end = kwargs.get('end', (0, 0))
        diag = kwargs.get('diag', False)
        if diag:
            self.D = self.D + self.DD

    def __repr__(self) -> str:
        out = ''
        for r in range(self._R):
            for c in range(self._C):
                if self.valid((r, c)):
                    out += self._space
                else:
                    out += self._wall
            out += '\n'
        return out

    def valid(self, node) -> bool:
        '''Determine whether a given node is traversable.'''
        r, c = node
        if 0 <= r < self._R and 0 <= c < self._C:
            return self.G[r][c] == self._space
        return False

    def neighbours(self, node) -> None:
        '''
        Return a generator of valid neighbours (open spaces)
        of the current node.
        '''
        r, c = node
        for dr, dc in self.D:
            if self.valid(((rr := r + dr), (cc := c + dc))):
                yield (rr, cc)

    def cost(self) -> int:
        '''Cost to move to new node.'''
        return 1

    def h(self) -> int:
        '''A* heuristic.'''
        return 0

    def bfs(self) -> None:
        '''Perform breadth-first search (BFS) on the graph.'''
        pass

    def dfs(self) -> None:
        '''Perform depth-first search (DFS) on the graph.'''
        pass

    def djikstra(self, h=lambda a, b: 0) -> None:
        '''Perform Djikstra's algorithm on the graph.'''
        cost = defaultdict(lambda: math.inf, {self.start: 0})
        prev = {}
        heapq.heappush(Q := [], (0, self.start))
        while Q:
            _, pos = heapq.heappop(Q)
            if pos == self.end:
                break
            for new_pos in self.neighbours(pos):
                new_cost = cost[pos] + self.cost()
                if new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    prev[new_pos] = pos
                    priority = new_cost + h(new_pos, self.end)
                    heapq.heappush(Q, (priority, new_pos))
        return cost[self.end]

    def astar(self) -> None:
        '''Perform A* search on the graph.'''
        return self.djikstra(h=self.h)

    def construct_path(self) -> set | None:
        '''
        Return a set of nodes (r, c) that comprise the optimal
        path from self.start to self.end.
        If self.end is None, return the set of visited nodes.
        '''
        pass

    def visualise_path(self, path) -> str:
        '''
        Return a string representation of the path traced
        by the set of nodes passed as the argument.
        '''
        pass

    def x(data, start, target=None, max_steps=None, astar=False, vis=False):

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


def main():
    pass


if __name__ == '__main__':
    main()
