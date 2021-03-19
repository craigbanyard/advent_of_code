from helper import aoc_timer
from collections import deque
from math import inf
import itertools
import re


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


@aoc_timer
def Day18(data, part2=False):

    # Constants
    R, C = len(data), len(data[0])
    START = '@1234'
    TRAVERSABLE = '.' + START
    KEYS = frozenset(re.findall(r"[a-z]", "".join(data)))
    POI = frozenset(START).union(KEYS)
    DIRS = [
        (-1, 0),    # North
        (0, 1),     # East
        (1, 0),     # South
        (0, -1)     # West
    ]
    ROBOTS = {
        '1': (-1, -1),
        '2': (-1, 1),
        '3': (1, 1),
        '4': (1, -1)
    }

    def distances(data, source):
        """
        Compile a dictionary where the keys are all points of interest
        (keys [a-z] and doors [A-Z]) and the values are the distances
        from the source to those points and the routes taken.
        """
        r0, c0 = source
        visited = set((r0, c0))
        Q = deque([(r0, c0, 0, "")])
        result = {}

        # BFS
        while Q:
            r, c, dist, route = Q.popleft()
            point = data[r][c]
            if point not in TRAVERSABLE and dist > 0:
                result[point] = (dist, route)
                route += point
            visited.add((r, c))
            for dr, dc in DIRS:
                rr = r + dr
                cc = c + dc
                if data[rr][cc] != '#' and (rr, cc) not in visited:
                    Q.append((rr, cc, dist + 1, route))
        return result

    def all_distances(data):
        """Return distances dictionary for all keys plus starting positions."""
        result = {}
        for r, c in itertools.product(range(R), range(C)):
            point = data[r][c]
            if point in POI:
                result[point] = distances(data, (r, c))
        return result

    def update_map(data):
        """Update the map for part 2."""
        data = [list(line) for line in data]
        for r, c in itertools.product(range(R), range(C)):
            if data[r][c] == '@':
                # Wall up
                data[r][c] = '#'
                for dr, dc in DIRS:
                    data[r + dr][c + dc] = '#'
                # Add robots
                for robot, (dr, dc) in ROBOTS.items():
                    data[r + dr][c + dc] = robot
                return ["".join(line) for line in data]

    # Initial setup
    if part2:
        data = update_map(data)
        init = tuple(ROBOTS.keys())
    else:
        init = tuple('@')

    # Solve maze
    routes = all_distances(data)
    Q = {(init, frozenset()): 0}
    for _ in range(len(KEYS)):
        new_Q = {}
        for (curr_loc, curr_keys), curr_dist in Q.items():
            for k in KEYS - curr_keys:
                # For part 1, this wil process just one location
                # For part 2, this will cycle the location of each robot
                for robot, loc in enumerate(curr_loc):
                    if k not in routes[loc]:
                        continue
                    dist, route = routes[loc][k]
                    if not all(c.lower() in curr_keys for c in route):
                        continue
                    new_dist = curr_dist + dist
                    new_keys = frozenset(k).union(curr_keys)
                    if part2:
                        # tuple -> list -> tuple because tuples are immutable
                        # (and lists aren't hashable)
                        new_loc = list(curr_loc)
                        new_loc[robot] = k
                        new_k = tuple(new_loc)
                    else:
                        new_k = k
                    if new_dist < new_Q.get((new_k, new_keys), inf):
                        new_Q[(new_k, new_keys)] = new_dist
        Q = new_Q

    return min(Q.values())


# %% Output
def main():
    print("AoC 2019\nDay 18")
    data = get_input('input.txt')
    print("Part 1:", Day18(data))
    print("Part 2:", Day18(data, part2=True))


if __name__ == '__main__':
    main()
