from time import time
from itertools import groupby
from collections import defaultdict
from os import getcwd


def get_input(path):
    adapters = [0] + [int(x.strip()) for x in open(path).readlines()]
    adapters.append(max(adapters)+3)
    return sorted(adapters)


def part1(data):
    deltas = []
    for idx, adapt in enumerate(data[1:]):
        deltas.append(adapt - data[idx])
    return deltas.count(1) * deltas.count(3)


def part2(data):
    data = sorted(set(data))
    routes = defaultdict(int)
    routes[max(data)] = 1
    for adapt in reversed(data):
        for jmp in (1, 2, 3):
            if adapt + jmp in data:
                routes[adapt] += routes[adapt+jmp]
    return routes[0]


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day10.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day10_3.txt"
    print("AoC 2020\nDay 10\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    print("Part 1:", part1(data))
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    print("Part 2:", part2(data))
    print("Time:", time() - t0)


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

def get_input_orig(path):
    return sorted(int(x.strip()) for x in open(path).readlines())


def part1_orig(data):
    deltas = [data[0]]
    for ad1, ad2 in zip(data, data[1:]):
        deltas.append(ad2-ad1)
    return deltas.count(1) * (deltas.count(3) + 1), deltas


# This doesn't work for group lengths higher than four
# Luckily, there aren't any such groups in my input
# The part that would fail is the 'arr *= (2**gl-n)' line, n isn't high enough for gl > 3
# Have created a part2_fix based on tribonacci sequence
def part2_orig(deltas):
    arr = 1
    for k, g in groupby(deltas):
        if k == 1:
            gl = len(list(g))-1
            n = max(0, gl - 2)
            arr *= (2**gl - n)
    return arr


# Turns out that the multiplications are elements of the tribonacci sequence
def trib(n):
    if n < 3:
        return 0
    if n == 3:
        return 1
    return trib(n-3) + trib(n-2) + trib(n-1)


def trib_alt(n):
    T = [0, 0, 1]
    i = 3
    while i < n:
        T += [sum(T[i-3:i])]
        i += 1
    return T[-1]


def trib_alt2(n):
    if n < 1:
        return

    t1, t2, t3 = 0, 0, 1
    if n < 3:
        return t1
    if n == 3:
        return t3

    for i in range(3, n):
        ans = t1 + t2 + t3
        t1 = t2
        t2 = t3
        t3 = ans

    return ans


def part2_fix(deltas):
    arr = 1
    for k, g in groupby(deltas):
        if k == 1:
            arr *= trib_alt2(len(list(g)) + 3)
    return arr


def orig():
    path = getcwd() + "\\Inputs\\Day10.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day10_3.txt"
    print("AoC 2020\nDay 10\n-----")
    t0 = time()
    data = get_input_orig(path)
    print("Data:", time() - t0, "\n-----")
    p1, deltas = part1_orig(data)
    print("Part 1:", p1)
    print("Time:", time() - t0, '\n-----')
    print("Part 2:", part2_fix(deltas))
    print("Time:", time() - t0)


'''
%timeit get_input_orig(path)
153 µs ± 547 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit part1_orig(data)
12 µs ± 291 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

%timeit part2_fix(deltas)
29.6 µs ± 105 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
'''
