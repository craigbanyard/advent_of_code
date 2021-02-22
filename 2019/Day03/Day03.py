from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [line.strip().split(",") for line in open(path).readlines()]


def draw_wire(wire):
    W = {}
    D = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }
    x, y, d = 0, 0, 0
    for i in wire:
        # (x, y) co-ordinate incrememnts and total distance
        dx, dy = D[i[0]]
        for _ in range(int(i[1:])):
            d += 1
            x += dx
            y += dy
            if (x, y) not in W:
                # Only add the first occurrence of location
                W[(x, y)] = d
    return W


@aoc_timer
def Day03(data, part1=True):
    # Steps to each point
    d1, d2 = list(map(draw_wire, data))
    # Wire intersections
    intersections = d1.keys() & d2.keys()
    # Part 1: Manhattan distance
    if part1:
        return min(abs(x) + abs(y) for x, y in intersections)
    # Part 2: Steps taken
    return min(d1[(x, y)] + d2[(x, y)] for x, y in intersections)


# %% Output
def main():
    print("AoC 2019\nDay 03")
    data = get_input('input.txt')
    print("Part 1:", Day03(data))
    print("Part 2:", Day03(data, part1=False))


if __name__ == '__main__':
    main()
