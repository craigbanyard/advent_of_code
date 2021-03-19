from helper import aoc_timer
from collections import deque, defaultdict
import itertools
import string


@aoc_timer
def get_input(path):
    return [x.strip('\n') for x in open(path).readlines()]


@aoc_timer
def Day20(data, part1=True, output=False):

    # Constants
    R, C = len(data), len(data[0])
    LETTERS = frozenset(string.ascii_uppercase)
    DIRS = [
        (-1, 0),    # North
        (0, 1),     # East
        (1, 0),     # South
        (0, -1)     # West
    ]
    START = 'AA'
    END = 'ZZ'

    # Inner corners for part 2
    inner = set()
    for r, line in enumerate(data[2:-2], start=2):
        if line[2:-2].count(' ') > 0:
            inner.add(r)
    IN_ROWS = range(
        min(inner) - 1,
        max(inner) + 2
    )
    IN_COLS = range(
        data[min(IN_ROWS) + 1][2:-2].find('# ') + 2,
        data[min(IN_ROWS) + 1][2:-2].find(' #') + 4
    )

    def level_diff(coords):
        """Return difference in maze level from entering portal at coords."""
        if part1:
            return 0
        r, c = coords
        if r in IN_ROWS and c in IN_COLS:
            return 1
        else:
            return -1

    # Dictionary of entry and exit points of all portals
    portals = defaultdict(list)
    for r, c in itertools.product(range(R-1), range(C-1)):
        if (p := data[r][c]) not in LETTERS:
            continue
        # Try reading down
        if (q := data[r + 1][c]) in LETTERS:
            if r < R - 2 and data[r + 2][c] == '.':
                rr = r + 2
            else:
                rr = r - 1
            portals[p + q].append((rr, c))
        # Try reading right
        elif (q := data[r][c + 1]) in LETTERS:
            if c < C - 2 and data[r][c + 2] == '.':
                cc = c + 2
            else:
                cc = c - 1
            portals[p + q].append((r, cc))

    # Dictionary of {in: (level_diff, out, label)}
    # both forward & reverse for all portals
    P = {}
    for label, coords in portals.items():
        if label == START or label == END:
            continue
        IN, OUT = coords
        P[IN] = level_diff(IN), OUT, label
        P[OUT] = level_diff(OUT), IN, label

    # BFS
    start_coords = portals[START][0]
    end_coords = portals[END][0]
    visited = set()
    route = START
    Q = deque([(start_coords, 0, 0, route)])
    while Q:
        (r, c), d, level, route = Q.popleft()
        visited.add(((r, c), level))
        for dr, dc in DIRS:
            coords = (r + dr, c + dc)
            rr, cc = coords
            if coords == end_coords and level == 0:
                if output:
                    return d + 1, f"{route}=>{END}"
                return d + 1
            if (coords, level) in visited or data[rr][cc] != '.':
                continue
            if coords in P:
                dl, coords, label = P[coords]
                if (next_level := level + dl) < 0:
                    continue
                Q.append((coords, d + 2, next_level, f"{route}=>{label}"))
            else:
                Q.append((coords, d + 1, level, route))
    return None


# %% Output
def main():
    print("AoC 2019\nDay 20")
    data = get_input('input.txt')
    print("Part 1:", Day20(data))
    print("Part 2:", Day20(data, part1=False))


if __name__ == '__main__':
    main()
