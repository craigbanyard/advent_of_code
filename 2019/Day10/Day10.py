from helper import aoc_timer
from math import atan2, pi, sqrt


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def get_asts(field, ast):
    """Get coordinates of all asteroids in field."""
    asteroids = []
    for r in range(len(field)):
        for c in range(len(field[r])):
            if field[r][c] == ast:
                asteroids.append((r, c))
    return asteroids


def get_slope(a, b):
    """Get slope of line between two asteroids."""
    y0, x0 = a
    y1, x1 = b
    dy, dx = y0 - y1, x1 - x0
    return atan2(dy, dx)


def get_dist(a, b):
    """Get straight line distance between two asteroids."""
    y0, x0 = a
    y1, x1 = b
    dy, dx = y0 - y1, x0 - x1
    return sqrt(dx**2 + dy**2)


def ord_slope(a, b):
    """Get slope of line between two asteroids (transformed), distance and coordinates."""
    slope = (get_slope(a, b) + (3 * pi / 2)) % (2 * pi)
    if slope == 0:
        slope += 2 * pi
    return slope, -get_dist(a, b), b


def ast_id(ast):
    """Get unique ID for asteroid based on its coordinates."""
    y, x = ast
    return (100 * x) + y


@aoc_timer
def Day10(data, part1=True):
    # Part 1 - best position for monitoring station
    asteroids = get_asts(data, '#')
    # {k: v} - number of other asteroids visible (v) from a given asteroid (k)
    visible = {}
    for a in asteroids:
        ast_vis = set()
        for b in asteroids:
            if a != b:
                ast_vis.add(get_slope(a, b))
        visible[a] = len(ast_vis)
    station = max(visible, key=visible.get)

    if part1:
        return visible[station]

    # Part 2 - crack out the giant laser; time to vaporize
    Q = []
    for b in asteroids:
        if b != station:
            Q.append(ord_slope(station, b))

    Q = sorted(Q, reverse=True)
    i = 0
    last_vap = Q[i]
    vaporized = 1
    while vaporized < 200:
        i += 1
        slope, *_ = last_vap
        if Q[i][0] == slope:
            continue
        last_vap = Q[i]
        *_, coords = last_vap
        vaporized += 1
    return ast_id(coords)


# %% Output
def main():
    print("AoC 2019\nDay 10")
    data = get_input('input.txt')
    print("Part 1:", Day10(data))
    print("Part 2:", Day10(data, part1=False))


if __name__ == '__main__':
    main()
