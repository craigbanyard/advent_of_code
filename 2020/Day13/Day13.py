from helper import aoc_timer
import math


@aoc_timer
def get_input(path):
    lines = [x.strip() for x in open(path).readlines()]
    dep = int(lines[0])
    busses = lines[1].split(',')
    offsets = {int(bus): idx for idx, bus in enumerate(busses) if bus != 'x'}
    return dep, offsets


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


@aoc_timer
def part1(dep, offsets):
    best = math.inf
    for bus in offsets.keys():
        wait = bus - dep % bus
        if wait < best:
            best = wait
            ans = best * bus
    return ans


@aoc_timer
def part2(offsets):
    t = 0
    tstep = list(offsets.keys())[0]
    for bus, off in offsets.items():
        while True:
            if (t + off) % bus == 0:
                tstep = lcm(tstep, bus)
                break
            t += tstep
    return t


# %% Output
def main():
    print("AoC 2020\nDay 13")
    dep, offsets = get_input('input.txt')
    print("Part 1:", part1(dep, offsets))
    print("Part 2:", part2(offsets))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 124 µs ± 220 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

# %timeit part1(dep, offsets)
# 1.02 µs ± 1.94 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

# %timeit part2(offsets)
# 80.3 µs ± 103 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
