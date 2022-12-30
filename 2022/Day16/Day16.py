from helper import aoc_timer
from collections import defaultdict, deque
import itertools as it
import re


@aoc_timer
def get_input(path: str) -> tuple[dict[str, list[str]], dict[str, int]]:
    T = defaultdict(list)
    V = {}
    regexp = re.compile(r'([A-Z]{2}).+\=(\d+)|([A-Z]{2})')
    for line in open(path).read().splitlines():
        for m in regexp.finditer(line):
            if m.group(1):
                v = m.group(1)
                V[v] = int(m.group(2))
            elif (vv := m.group(3)):
                T[v].append(vv)
    return T, V


def get_costs(data, start: str = 'AA') -> dict[str, int]:
    '''
    Perform BFS on the tunnel network to get the cost of
    visiting and opening each non-zero flow rate valve.
    '''
    T, V = data
    Q = deque([(start, 0)])
    visited = {}
    while Q:
        v, t = Q.popleft()
        if v in visited:
            continue
        visited[v] = t
        for vv in T[v]:
            Q.append((vv, t + 1))
    return {v: t for v, t in visited.items() if V[v] and v != start}


def prune(data, start: str = 'AA') -> dict[str, dict[str, int]]:
    '''
    Return a graph of distances between all pairs of non-
    zero flow rate valves.
    '''
    _, V = data
    graph = {}
    for v in V:
        if V[v] or v == start:
            graph[v] = get_costs(data, v)
    return graph


def dfs(graph: dict[str, dict[str, int]], V: dict[str, int],
        time_limit: int = 30) -> dict[frozenset[str], int]:
    '''
    Perform DFS on the pruned graph and return the dictionary
    of visited states mapped to their maximum pressure relief.
    Although the number of states visited is the same as under
    BFS, DFS is faster on average for this problem.
    '''
    # (Current valve, open valves, time remaining, pressure released)
    start = ('AA', frozenset(), time_limit, 0)
    visited = defaultdict(int)

    def _dfs(v: str, o: frozenset[str], t: int, p: int) -> None:
        '''
        Recursive DFS utility function.
        Mutates the visited dictionary.
        '''
        visited[o] = max(visited[o], p)
        for valve, cost in graph[v].items():
            if (tt := t - cost - 1) <= 0:
                return None
            if valve not in o:
                _dfs(valve, o.union([valve]), tt, p + V[valve] * tt)

    # Populate the visited dictionary by calling _dfs
    _dfs(*start)
    return visited


def bfs(graph: dict[str, dict[str, int]], V: dict[str, int],
        time_limit: int = 30) -> dict[frozenset[str], int]:
    '''
    Perform BFS on the pruned graph and return the dictionary
    of visited states mapped to their maximum pressure relief.
    Although the number of states visited is the same as under
    DFS, BFS is slower on average for this problem.
    '''
    # (Current valve, open valves, time remaining, pressure released)
    start = ('AA', frozenset(), time_limit, 0)
    visited = defaultdict(int)
    Q = deque([(start)])
    while Q:
        v, o, t, p = Q.popleft()
        visited[o] = max(visited[o], p)
        for valve, cost in graph[v].items():
            if (tt := t - cost - 1) <= 0:
                continue
            if valve not in o:
                Q.append((valve, o.union([valve]), tt, p + V[valve] * tt))
    return visited


@aoc_timer
def solve(data, elephant_threshold: int = 0) -> tuple[int, int]:
    _, V = data
    graph = prune(data, start='AA')
    p1 = max(dfs(graph, V, time_limit=30).values())
    p2 = 0
    # Optimisation: filter out paths that release less than a given
    # threshold pressure amount, since we assume that the elephant
    # would not be able to open enough valves to hit the required
    # maximum pressure release if we are below this threshold.
    visited = {k: v for k, v in dfs(graph, V, time_limit=26).items()
               if v > elephant_threshold}
    for (p, a), (q, b) in it.combinations(visited.items(), 2):
        if p.isdisjoint(q):
            p2 = max(p2, a + b)
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 16")
    data = get_input('input.txt')
    p1, p2 = solve(data, elephant_threshold=1000)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
