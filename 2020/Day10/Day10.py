from helper import aoc_timer
from collections import defaultdict


@aoc_timer
def get_input(path):
    adapters = [0] + [int(x.strip()) for x in open(path).readlines()]
    adapters.append(max(adapters) + 3)
    return sorted(adapters)


@aoc_timer
def part1(data):
    deltas = []
    for idx, adapt in enumerate(data[1:]):
        deltas.append(adapt - data[idx])
    return deltas.count(1) * deltas.count(3)


@aoc_timer
def part2(data):
    data = sorted(set(data))
    routes = defaultdict(int)
    routes[max(data)] = 1
    for adapt in reversed(data):
        for jmp in (1, 2, 3):
            if adapt + jmp in data:
                routes[adapt] += routes[adapt + jmp]
    return routes[0]


# %% Output
def main():
    print("AoC 2020\nDay 10")
    data = get_input('input.txt')
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 163 µs ± 575 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

# %timeit part1(data)
# 13.5 µs ± 258 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

# %timeit part2(data)
# 317 µs ± 1.64 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
