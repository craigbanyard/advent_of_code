from helper import aoc_timer
from collections import defaultdict
import heapq
import math


@aoc_timer
def get_input(path):
    G = []
    for line in open(path).read().splitlines():
        G.append([*map(int, [*line])])
    return G


@aoc_timer
def Day15(G, n=1, astar=False):

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

    cost = defaultdict(lambda: math.inf, {START: 0})
    heapq.heappush(Q := [], (0, START))

    while Q:
        _, pos = heapq.heappop(Q)
        if pos == END:
            break
        for new_pos in neighbours(pos):
            new_risk = cost[pos] + risk(new_pos)
            if new_risk < cost[new_pos]:
                cost[new_pos] = new_risk
                priority = new_risk + h(new_pos, END)
                heapq.heappush(Q, (priority, new_pos))
    return cost[END]


# %% Output
def main():
    print("AoC 2021\nDay 15")
    data = get_input('input.txt')
    print("Part 1:", Day15(G=data, n=1, astar=False))
    print("Part 2:", Day15(G=data, n=5, astar=False))


if __name__ == '__main__':
    main()
