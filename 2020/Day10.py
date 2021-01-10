from helper import aoc_timer
from itertools import groupby
from collections import defaultdict
from os import getcwd


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
    path = getcwd() + "\\Inputs\\Day10.txt"
    data = get_input(path)
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
163 µs ± 575 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit part1(data)
13.5 µs ± 258 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

%timeit part2(data)
317 µs ± 1.64 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''


# %% Original code
@aoc_timer
def get_input_orig(path):
    return sorted(int(x.strip()) for x in open(path).readlines())


@aoc_timer
def part1_orig(data):
    deltas = [data[0]]
    for ad1, ad2 in zip(data, data[1:]):
        deltas.append(ad2-ad1)
    return deltas.count(1) * (deltas.count(3) + 1), deltas


# Dynamic programming recursive tribonacci
def trib(n, DP={0: 0, 1: 0, 2: 0, 3: 1}):
    if n not in DP:
        DP[n] = trib(n-3) + trib(n-2) + trib(n-1)
    return DP[n]


# Iterative tribonacci
def trib2(n):
    if n <= 3:
        return n // 3
    t1, t2, t3 = 0, 0, 1
    for i in range(3, n):
        t1, t2, t3 = t2, t3, t1 + t2 + t3
    return t3


# Turns out that the coefficients are elements of the tribonacci sequence
@aoc_timer
def part2_orig(deltas):
    arr = 1
    for k, g in groupby(deltas):
        if k == 1:
            arr *= trib(len(list(g)) + 3)
    return arr


# %% Original output
def main_orig():
    print("AoC 2020\nDay 10")
    path = getcwd() + "\\Inputs\\Day10.txt"
    data = get_input_orig(path)
    p1, deltas = part1_orig(data)
    print("Part 1:", p1)
    print("Part 2:", part2_orig(deltas))


# main_orig()


'''
%timeit get_input_orig(path)
147 µs ± 242 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit part1_orig(data)
12 µs ± 291 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

%timeit part2_orig(deltas)
14.8 µs ± 40.9 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
'''
