from helper import aoc_timer
from itertools import permutations
from math import inf


@aoc_timer
def get_input(path):
    return [x.strip().split()[::2] for x in open(path).readlines()]


# Function used to discard routes that are the reverse of other routes
# This halves the number of permutations (iterations) required to find shortest/longest route
def get_unique_perms(locations):
    """Discard routes that are the reverse of other routes.
       This halves the number of permutations (iterations) required to find route.
    """
    for p in permutations(locations):
        if p <= p[::-1]:
            yield p


@aoc_timer
def Day09(data):
    D = {}
    for a, b, d in data:
        # Add distances (both directions, saves check within loop) to dictionary
        D[(a, b)] = D[(b, a)] = int(d)
    L = set(v for k in D for v in k)
    shortest, longest = inf, 0
    for p in get_unique_perms(L):
        dist = sum(D[(a, b)] for a, b in zip(p, p[1:]))
        shortest = min(dist, shortest)
        longest = max(dist, longest)
    return shortest, longest


# %% Output
def main():
    print("AoC 2015\nDay 09")
    data = get_input('input.txt')
    p1, p2 = Day09(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
