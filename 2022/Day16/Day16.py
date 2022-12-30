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


# Alternative solution using integers to represent valves and states.
def enumerate_valves(V: dict[str, int]) -> dict[str, int]:
    '''
    Assign an integer index to each valve based on their flow
    rate. AA is assigned index 0.
    '''
    sorted_valves = sorted(V, key=V.get, reverse=True)
    result = {'AA': 0}
    for idx, v in enumerate(sorted_valves, start=1):
        if v not in result:
            result[v] = idx
    return result


def valves_as_int(V: dict[str, int], enum_valves: dict[str, int]) -> list[int]:
    '''
    Return a list of valve flow rates, where each valve is
    represented by its index in the list.
    '''
    return [V[v] for v in sorted(enum_valves, key=enum_valves.get)]


def graph_as_int(graph: dict[str, dict[str, int]],
                 enum_valves: dict[str, int]) -> list[dict[int, int]]:
    '''Convert a string-based graph to an integer-based graph.'''
    result = [[] for _ in range(len(graph))]
    for k, v in graph.items():
        result[enum_valves[k]] = {enum_valves[vv]: v[vv] for vv in v}
    return result


def is_closed(valve: int, open_valves: int) -> bool:
    '''
    Determine whether a valve is closed using bit-shifting.
    Left shift 1 by the valve index (k) to create an integer
    where only the kth bit is set to 1.
    Bitwise AND this result with the open valves to determine
    whether there are any bits in common.
    If there are no bits in common, the valve is closed.
    '''
    return not open_valves & (1 << valve)


def dfs_alt(graph: list[dict[int, int]], V: list[int],
            time_limit: int = 30) -> dict[int, int]:
    '''
    Perform DFS on the pruned graph and return the dictionary
    of visited states mapped to their maximum pressure relief.
    This implementation uses integers to represent the valves
    and the set of open valves is stored as a single integer
    by treating each open valve as a unique power of 2. This
    is much faster than performing set unions.
    '''
    # (Current valve, open valves, time remaining, pressure released)
    start = (0, 0, time_limit, 0)
    visited = defaultdict(int)

    def _dfs(v: int, o: int, t: int, p: int) -> None:
        '''
        Recursive DFS utility function.
        Mutates the visited dictionary.
        '''
        visited[o] = max(visited[o], p)
        for valve, cost in graph[v].items():
            if (tt := t - cost - 1) <= 0:
                return None
            if is_closed(valve, o):
                _dfs(valve, o + 2**valve, tt, p + V[valve] * tt)

    # Populate the visited dictionary by calling _dfs
    _dfs(*start)
    return visited


@aoc_timer
def solve_alt(data, elephant_threshold: int = 0) -> tuple[int, int]:
    _, V = data
    enum_valves = enumerate_valves(V)
    V = valves_as_int(V, enum_valves)
    graph = graph_as_int(prune(data, start='AA'), enum_valves)
    p1 = max(dfs_alt(graph, V, time_limit=30).values())
    p2 = 0
    # Optimisation: filter out paths that release less than a given
    # threshold pressure amount, since we assume that the elephant
    # would not be able to open enough valves to hit the required
    # maximum pressure release if we are below this threshold.
    visited = {k: v for k, v in dfs_alt(graph, V, time_limit=26).items()
               if v > elephant_threshold}
    for (p, a), (q, b) in it.combinations(visited.items(), 2):
        if not p & q:
            p2 = max(p2, a + b)
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 16")
    data = get_input('input.txt')
    print('\nOriginal solution:')
    p1, p2 = solve(data, elephant_threshold=1000)
    print("Part 1:", p1)
    print("Part 2:", p2)
    # Demonstrate solutions are equivalent
    print('\nAlternative solution:')
    p1, p2 = solve_alt(data, elephant_threshold=1000)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
