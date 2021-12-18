from helper import aoc_timer, Colours
from collections import defaultdict
import heapq
import itertools
import math


@aoc_timer
def get_input(path):
    G = []
    for line in open(path).read().splitlines():
        G.append([*map(int, [*line])])
    return G


@aoc_timer
def Day15(G, n=1, astar=False, vis=False):

    D = [
        (-1, 0),    # Up
        (0, 1),     # Right
        (1, 0),     # Down
        (0, -1)     # Left
    ]

    RR, CC = len(G), len(G[0])
    R, C = RR * n, CC * n
    START, END = (0, 0), (R - 1, C - 1)

    def neighbours(pos):
        '''Return a generator of valid neighbours of pos.'''
        r, c = pos
        for dr, dc in D:
            if 0 <= (rr := r + dr) < R and 0 <= (cc := c + dc) < C:
                yield (rr, cc)

    def h(a, b):
        '''A* heuristic: Manhattan distance between points a and b.'''
        if astar:
            return sum(abs(p - q) for p, q in zip(a, b))
        return 0

    def risk(pos):
        '''Return the risk associated with position pos in the cave.'''
        (dr, r), (dc, c) = map(divmod, pos, (RR, CC))
        return (G[r][c] + dr + dc) % 9 or 9

    def construct_path(paths, start, end):
        '''
        Return a set of coordinates (r, c) that comprise
        the optimal path from start to end.
        '''
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
        grid = ''
        highlight = Colours.BOLD + Colours.fg.CYAN
        for pos in itertools.product(range(R), range(C)):
            if pos[1] == 0:
                grid += '\n'
            if pos in path:
                grid += f'{highlight}{risk(pos)}{Colours.ENDC}'
            else:
                grid += f'{risk(pos)}'
        return grid + '\n'

    cost = defaultdict(lambda: math.inf, {START: 0})
    prev = {}
    heapq.heappush(Q := [], (0, START))

    # Djikstra (or A* if heuristic is used)
    while Q:
        _, pos = heapq.heappop(Q)
        if pos == END:
            break
        for new_pos in neighbours(pos):
            new_risk = cost[pos] + risk(new_pos)
            if new_risk < cost[new_pos]:
                cost[new_pos] = new_risk
                prev[new_pos] = pos
                priority = new_risk + h(new_pos, END)
                heapq.heappush(Q, (priority, new_pos))
    if vis:
        optimal_path = construct_path(prev, START, END)
        print(visualise(optimal_path))
    return cost[END]


# %% Output
def main():
    print("AoC 2021\nDay 15")
    data = get_input('input.txt')
    print("Part 1:", Day15(G=data, n=1, astar=False, vis=True))
    print("Part 2:", Day15(G=data, n=5, astar=False, vis=False))


if __name__ == '__main__':
    main()
