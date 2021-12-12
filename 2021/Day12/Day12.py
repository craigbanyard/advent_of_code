from helper import aoc_timer
from collections import defaultdict, deque


START, END = 'start', 'end'


@aoc_timer
def get_input(path: str) -> dict[str, set[str]]:
    G = defaultdict(set)
    for line in open(path).read().splitlines():
        a, b = line.split('-')
        G[a].add(b)
        G[b].add(a)
    # Reduce search space by preventing backtracking to START
    for n in G[START]:
        G[n].discard(START)
    # Remove unnecessary edges - END is an absorbing vertex
    del G[END]
    return G


@aoc_timer
def Day12(G: dict[str, set[str]]) -> tuple[int, int]:
    p1 = p2 = 0
    initial = (START, set([START]), False)
    Q = deque([initial])
    while Q:
        cave, path, small_twice = Q.popleft()
        if cave == END:
            if not small_twice:
                p1 += 1
            p2 += 1
            continue
        for c in G[cave]:
            if c not in path:
                # Reduce search space - only track small caves
                if c.islower():
                    Q.append((c, path | {c}, small_twice))
                else:
                    Q.append((c, path, small_twice))
            elif not small_twice:
                Q.append((c, path, True))
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 12")
    data = get_input('input.txt')
    p1, p2 = Day12(G=data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
