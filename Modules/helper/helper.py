from collections import defaultdict, deque
from functools import wraps, partial
import heapq
import math
import numpy as np
from time import perf_counter_ns
from typing import Iterator


class Colours:
    '''ANSI code class for terminal highlighting.'''

    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    HIDE = '\033[8m'
    STRIKE = '\033[9m'

    class fg:
        '''Foreground colours.'''

        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        ORANGE = '\033[33m'
        BLUE = '\033[34m'
        PURPLE = '\033[35m'
        CYAN = '\033[36m'
        LIGHTGREY = '\033[37m'
        DARKGREY = '\033[90m'
        LIGHTRED = '\033[91m'
        LIGHTGREEN = '\033[92m'
        YELLOW = '\033[93m'
        LIGHTBLUE = '\033[94m'
        PINK = '\033[95m'
        LIGHTCYAN = '\033[96m'

    class bg:
        '''Background colours.'''

        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        ORANGE = '\033[43m'
        BLUE = '\033[44m'
        PURPLE = '\033[45m'
        CYAN = '\033[46m'
        LIGHTGREY = '\033[47m'

    def __repr__(self) -> str:
        '''Demo of usage of the class.'''
        def attrs_to_str(cls, label) -> str:
            '''
            Return a string representation of the public attributes of cls with
            type str.
            '''
            out = f'{label}\n'
            attrs = {k: v for k, v in vars(cls).items()
                     if not k.startswith('__') and isinstance(v, str)}
            for k, v in attrs.items():
                out += f'{k}: {v}{k}{self.ENDC}\n'
            out += '\n'
            return out

        classes = [Colours, Colours.fg, Colours.bg]
        labels = ['Styles', 'Foregrounds', 'Backgrounds']
        return ''.join([attrs_to_str(cls, label)
                        for cls, label in zip(classes, labels)])


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
        '''
        Grid class based on row, column (r, c) layout.
        Keyword arguments:
          G: List of lists representing the grid
          space: String representing traversable space
          wall: String representing non-traversable space
          diag: Indiactor of whether diagonal moves are valid
        '''
        self.G = kwargs.get('G', [[]])
        self._R = len(self.G)
        self._C = len(self.G[0])
        self.grid_dict = {(r, c): self.G[r][c]
                          for c in range(self._C)
                          for r in range(self._R)}
        self._space = kwargs.get('space', '.')
        self._wall = kwargs.get('wall', '#')
        if kwargs.get('diag', False):
            self.D = self.D + self.DD

    def __repr__(self) -> str:
        '''String representation of the grid.'''
        out = ''
        for r in range(self._R):
            for c in range(self._C):
                if self.valid((r, c)):
                    out += self._space
                else:
                    out += self._wall
            out += '\n'
        return out

    def items(self) -> dict:
        '''Allow simple iteration over the grid coordinates and values.'''
        return self.grid_dict.items()

    def where(self, value) -> Iterator[tuple]:
        '''Return a generator of nodes with the given value.'''
        for (r, c), v in self.items():
            if v == value:
                yield (r, c)

    def _init_traversal(self, start) -> list[tuple]:
        '''Initialise start position(s) for grid traversal.'''
        match start:
            case (int(), int()):
                return [start]
            case [(int(), int()), *_]:
                return start
            case value:
                return list(self.where(value))

    def _init_cost_dict(self, start_nodes) -> dict[tuple, int]:
        '''Initialise cost dictionary for grid traversal.'''
        return defaultdict(lambda: math.inf, {s: 0 for s in start_nodes})

    def _traversal_complete(self, node, cost, end, max_cost) -> bool:
        '''
        Determine whether the end conditions of the traversal are satisfied.
        '''
        if cost[node] >= max_cost:
            return True
        match end:
            case int(), int():
                return node == end
            case (int(), int()), *_:
                return node in end
            case None:
                return False
            case value:
                r, c = node
                return self.G[r][c] == value

    def valid(self, node) -> bool:
        '''Determine whether a given node is traversable.'''
        r, c = node
        if 0 <= r < self._R and 0 <= c < self._C:
            return self.G[r][c] == self._space
        return False

    def neighbours(self, node) -> Iterator[tuple]:
        '''
        Return a generator of valid neighbours (open spaces) of the current
        node.
        '''
        r, c = node
        for dr, dc in self.D:
            if self.valid(((rr := r + dr), (cc := c + dc))):
                yield (rr, cc)

    def cost(self, node) -> int:
        '''Cost to move to node.'''
        return 1

    def h(self, a, b) -> int:
        '''
        A* heuristic for moving between nodes a and b.
        Default implementation is Manhattan distance.
        '''
        return sum(abs(p - q) for p, q in zip(a, b))

    def bfs(self, start, end, max_cost=math.inf) -> tuple[dict, dict]:
        '''Perform breadth-first search (BFS) on the grid.'''
        visited = {}
        start_nodes = self._init_traversal(start)
        cost = self._init_cost_dict(start_nodes)
        Q = deque([*start_nodes])
        while Q:
            pos = Q.popleft()
            if self._traversal_complete(pos, cost, end, max_cost):
                break
            for new_pos in self.neighbours(pos):
                new_cost = cost[pos] + self.cost(new_pos)
                if new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    visited[new_pos] = pos
                    Q.append(new_pos)
        return visited, cost

    def dfs(self, start, end, max_cost=math.inf) -> tuple[dict, dict]:
        '''Perform depth-first search (DFS) on the grid.'''
        visited = {}
        start_nodes = self._init_traversal(start)
        cost = self._init_cost_dict(start_nodes)

        def _dfs(visited, cost, pos):
            if self._traversal_complete(pos, cost, end, max_cost):
                return visited, cost
            for new_pos in self.neighbours(pos):
                new_cost = cost[pos] + self.cost(new_pos)
                if new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    visited[new_pos] = pos
                    return _dfs(visited, cost, new_pos)
            return visited, cost

        for start in start_nodes:
            # Probably needs revising in light of multiple starts...
            return _dfs(visited, cost, start)

    def djikstra(self, start, end, h=lambda a, b: 0,
                 max_cost=math.inf) -> tuple[dict, dict]:
        '''Perform Djikstra's algorithm on the grid.'''
        visited = {}
        start_nodes = self._init_traversal(start)
        cost = self._init_cost_dict(start_nodes)
        Q = []
        for start in start_nodes:
            heapq.heappush(Q, (0, start))
        while Q:
            _, pos = heapq.heappop(Q)
            if self._traversal_complete(pos, cost, end, max_cost):
                break
            for new_pos in self.neighbours(pos):
                new_cost = cost[pos] + self.cost(new_pos)
                if new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    visited[new_pos] = pos
                    priority = new_cost + h(new_pos, end)
                    heapq.heappush(Q, (priority, new_pos))
        return visited, cost

    def astar(self, start, end, h=None, max_cost=math.inf) -> tuple[dict, dict]:
        '''Perform A* search on the grid.'''
        if h is None:
            h = self.h
        return self.djikstra(start, end, h, max_cost)

    def run_algorithm(self, start, end, algorithm) -> tuple[dict, dict]:
        '''
        Run the specified algorithm for the specified start and end nodes.
        '''
        algorithms = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'djikstra': self.djikstra,
            'astar': self.astar
        }
        f = algorithms.get(algorithm.lower(), lambda a, b: ({}, {}))
        return f(start, end)

    def shortest_path(self, start, end, algorithm) -> int:
        '''
        Return the shortest path from start to end as computed by the specified
        algorithm.
        '''
        _, cost = self.run_algorithm(start, end, algorithm)
        match end:
            case int(), int():
                return cost[end]
            case int(), int(), *_:
                return min(cost[e] for e in end)
            case value:
                return min(cost[v] for v in self.where(value))

    def construct_path(self, start, end, visited) -> set:
        '''
        Return a set of nodes (r, c) that comprise the path from start to end
        implied by the visited dictionary.
        If end is None, return the set of visited nodes.
        '''
        if end is None:
            return set(visited.keys()) | {start}
        if end not in visited:
            return set()
        c = end
        path = set([c])
        while c in visited:
            c = visited[c]
            path.add(c)
            if c == start:
                return path
        return set()

    def optimal_path(self, start, end, algorithm) -> set:
        '''
        Return a set of nodes (r, c) that comprise the optimal path from start
        to end determined by performing the specified search algorithm.
        If end is None, return the set of visited nodes.
        '''
        visited, _ = self.run_algorithm(start, end, algorithm)
        return self.construct_path(start, end, visited)

    def visualise_path(self, path, **kwargs) -> str | None:
        '''
        Return a string representation of the path provided as the argument.
        Optimal path marker can be provided as the marker keyword argument.
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
        _marker = f'{Colours.BOLD + Colours.fg.CYAN}O{Colours.ENDC}'
        marker = kwargs.get('marker', _marker)
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                if (r, c) in path:
                    grid += marker
                elif self.valid((r, c)):
                    grid += self._space
                else:
                    grid += self._wall
            grid += '\n'
        return grid


def aoc_timer(func=None, *, repeat=1, metric=min, **margs):
    '''
    Decorator that times the call of a function, func, and prints its execution
    time. If func is called with keyword argument time=False, the print will be
    surpressed.

    With optional repeat, run func repeat times, appending successive execution
    times to list (or numpy array) [times].
    With optional metric, apply the function metric to the array [times] to
    calculate execution time to display. Default is min, i.e. display minimum
    execution time.
      Expected built-ins: {min, max, list, sorted}
      Expected custom: {'mean', 'mean_std', 'std', 'var', ...}
      https://numpy.org/doc/stable/reference/routines.statistics.html
      Keyword arguments of metric must be specified as **margs.
    '''

    def format_time(t):
        units = ['ns', 'μs', 'ms', 's']
        if t < 1:
            return f"{float(t):.4} ns"
        digits = math.floor(math.log10(t))
        idx = min(len(units) - 1, digits // 3)
        return f"{float(t / 10**(3*idx)):.4} {units[idx]}"

    def mean_std(times):
        m, s = np.mean(times), np.std(times)
        return f"{format_time(m)} ± {format_time(s)}"

    # Handle invalid metrics
    def err(times, metric=metric):
        return f'Invalid metric: {metric}'

    if isinstance(metric, str):
        # Not using built-in => numpy likely quicker
        times = np.zeros(repeat)
        try:
            metric = locals()[metric]
        except KeyError:
            # Try numpy, else err
            metric = getattr(np, metric, err)
    else:
        # Using built-in => list likely quicker
        times = [None] * repeat

    if func is None:
        return partial(aoc_timer, repeat=repeat, metric=metric, **margs)

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        if kwargs.get("time") is False:
            return func(*args, **kwargs)

        for t in range(repeat):
            t0 = perf_counter_ns()
            result = func(*args, **kwargs)
            t1 = perf_counter_ns() - t0
            times[t] = t1

        if 'get_input' in func.__name__:
            label = 'Data'
        else:
            label = 'Time'

        disp = metric(times, **margs)
        # Check if disp is iterable before attempting to format time
        try:
            _ = iter(disp)
        except TypeError:
            # Not iterable => format time
            disp = format_time(disp)

        print(f"-----\n{label}: {disp}")
        return result

    return wrapper_timer


def sign(n: int) -> int:
    '''
    Return the sign of integer n:
      if n < 0:  -1
      if n == 0:  0
      if n > 0:   1
    '''
    if not n:
        return 0
    return n // abs(n)


def main():
    pass


if __name__ == '__main__':
    main()
