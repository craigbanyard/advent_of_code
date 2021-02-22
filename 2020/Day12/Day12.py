from helper import aoc_timer


@aoc_timer
def get_input(path):
    C = {'N': 1j, 'E': 1, 'S': -1j, 'W': -1}
    R = {
        'L': lambda x: x // 90,
        'R': lambda x: -(x // 90) % 4
    }
    for line in open(path).read().split('\n'):
        head, unit = line[0], int(line[1:])
        if head in C:
            yield (None, unit * C[head])
        elif head in R:
            yield (True, 1j ** R[head](unit))
        else:
            yield (False, unit)


def manhattan(c):
    return int(abs(c.real) + abs(c.imag))


@aoc_timer
def Day12(path):
    # Starting position of ship and waypoint
    p1, w1 = 0, 1 + 0j
    p2, w2 = 0, 10 + 1j
    for head, unit in get_input(path):
        if head is None:
            # Move in a direction
            p1 += unit
            w2 += unit
        elif head:
            # Rotation
            w1 *= unit
            w2 *= unit
        else:
            # Move forwards
            p1 += w1 * unit
            p2 += w2 * unit
    return manhattan(p1), manhattan(p2)


# %% Output
def main():
    print("AoC 2020\nDay 12")
    p1, p2 = Day12('input.txt')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 283 ns ± 1.18 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

# %timeit Day12('input.txt')
# 777 µs ± 1.31 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
