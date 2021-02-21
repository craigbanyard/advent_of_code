from helper import aoc_timer


@aoc_timer
def get_input(path):
    return open(path).read()


def move(d):
    dirs = {
        '^': (0, 1),
        'v': (0, -1),
        '>': (1, 0),
        '<': (-1, 0)
    }
    return dirs[d]


def p1(data):
    # Starting point
    x, y = 0, 0
    # Visited houses
    visited = {(x, y)}
    for d in data:
        dx, dy = move(d)
        x += dx
        y += dy
        visited.add((x, y))
    return len(visited)


def p2(data):
    # Starting points
    xS, xR, yS, yR = 0, 0, 0, 0
    # Visited houses
    visited = {(xS, yS)}
    # Take pairwise directions
    for S, R in zip(data[0::2], data[1::2]):
        # Santa
        dxS, dyS = move(S)
        xS += dxS
        yS += dyS
        visited.add((xS, yS))
        # Robo-Santa
        dxR, dyR = move(R)
        xR += dxR
        yR += dyR
        visited.add((xR, yR))
    return len(visited)


@aoc_timer
def Day03(data, part2=False):
    if part2:
        return p2(data)
    return p1(data)


# %% Output
def main():
    print("AoC 2015\nDay 03")
    data = get_input('input.txt')
    print("Part 1:", Day03(data))
    print("Part 2:", Day03(data, part2=True))


if __name__ == '__main__':
    main()
