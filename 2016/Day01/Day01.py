from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [(x[0], int(x[1:])) for x in open(path).read().split(', ')]


def manhattan(pos):
    return int(abs(pos.real) + abs(pos.imag))


@aoc_timer
def Day01(data, part1=True):
    D = {
        'R': -1j,
        'L': 1j
    }
    heading, pos = 1j, 0
    visited = set()
    for (dir, dist) in data:
        heading *= D[dir]
        if part1:
            pos += heading * dist
            continue
        for i in range(dist):
            pos += heading
            if pos in visited:
                return manhattan(pos)
            visited.add(pos)
    return manhattan(pos)


# %% Output
def main():
    print("AoC 2016\nDay 01")
    data = get_input('input.txt')
    print("Part 1:", Day01(data))
    print("Part 2:", Day01(data, part1=False))


if __name__ == '__main__':
    main()
