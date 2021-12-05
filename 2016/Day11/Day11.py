from helper import aoc_timer
from collections import defaultdict
import heapq
from itertools import combinations
import re


FLOORS = range(4)


@aoc_timer
def get_input(path):
    R = re.compile(r'(\w+) generator|(\w+)-compatible')
    idx = 1
    elems = {}
    objs = defaultdict(set)
    for floor, line in enumerate(open(path).read().splitlines()):
        for match in re.finditer(R, line):
            # Generators (+ve numbers)
            if (g := match.group(1)):
                if g not in elems:
                    elems[g] = idx
                    idx += 1
                objs[floor].add(elems[g])
            # Microchips (-ve numbers)
            if (m := match.group(2)):
                if m not in elems:
                    elems[m] = idx
                    idx += 1
                objs[floor].add(-elems[m])
    # Items are sorted so checking for generators is quick
    # Returning as tuple as this is a hashable type
    return tuple([tuple(sorted(objs[k])) for k in FLOORS])


def safe(floor):
    """
    A floor is safe if:
    1. No items
    2. No generators
    3. Every microchip is powered by a corresponding generator
    """
    if not floor or floor[-1] < 0:
        return True
    return all(-chip in floor for chip in floor if chip < 0)


def combs(floor):
    """Returns all 1-item and 2-item combinations of items on a floor."""
    return list(combinations(floor, 2)) + list(combinations(floor, 1))


@aoc_timer
def Day11(floors):
    DIRS = (-1, 1)
    START = (0, floors)
    Q = []

    heapq.heappush(Q, (0, START))
    cost = {START: 0}

    while Q:
        _, current = heapq.heappop(Q)
        f, floors = current

        if f == FLOORS[-1] and all(not x for x in floors[:-1]):
            # We are at the top floor and no items on other floors
            break

        dirs = [d for d in DIRS if (f + d) in FLOORS]
        for move in combs(floors[f]):
            for d in dirs:
                # Convert to mutable list
                new_floors = list(floors)
                # Remove moved items from current floor
                new_floors[f] = tuple(x for x in floors[f] if x not in move)
                # Add moved items to next floor
                new_floors[f + d] = tuple(sorted(floors[f + d] + move))

                if not safe(new_floors[f]) or not safe(new_floors[f + d]):
                    continue

                # Convert back to hashable tuple
                next = (f + d, tuple(new_floors))
                new_cost = cost[current] + 1
                if next not in cost or new_cost < cost[next]:
                    cost[next] = new_cost
                    # Heuristic factor (arbitrary)
                    priority = new_cost - len(new_floors[-1]) * 10
                    heapq.heappush(Q, (priority, next))

    return cost[current]


# %% Output
def main():
    print("AoC 2016\nDay 11")
    print("Part 1:", Day11(get_input('input.txt')))
    print("Part 2:", Day11(get_input('input2.txt')))


if __name__ == '__main__':
    main()
