from helper import aoc_timer
from os import getcwd


@aoc_timer
def get_input(path):
    return {int(x.strip()) for x in open(path).readlines()}


@aoc_timer
def Part1(data, target=2020, time=True):
    for x in data:
        y = target - x
        if y in data:
            return x * y


@aoc_timer
def Part2(data, target=2020):
    for x in data:
        y = Part1(data, target - x, time=False)
        if y is not None:
            return x * y


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day01.txt"
    print("AoC 2020\nDay 1")
    data = get_input(path)
    print("Part 1:", Part1(data))
    print("Part 2:", Part2(data))


if __name__ == '__main__':
    main()


'''
--- Timings using set for input data ---

%timeit get_input(path)
165 µs ± 352 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Part1(data)
3.54 µs ± 42.9 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

%timeit Part2(data)
17.7 µs ± 152 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
'''


# %% Other solutions
from itertools import combinations


@aoc_timer
def get_input_list(path):
    return [int(x.strip()) for x in open(path).readlines()]


@aoc_timer
def p1(data):
    return max(a * b for a, b in combinations(data, 2) if a + b == 2020)


@aoc_timer
def p2(data):
    return max(a * b * c for a, b, c in combinations(data, 3) if a + b + c == 2020)


@aoc_timer
def faster_p1(data):
    return max(x * (2020 - x) for x in data if (2020 - x) in data)


@aoc_timer
def faster_p2(data):
    return max(x * y * (2020 - x - y) for x in data for y in data if (2020 - x - y) in data)


'''
--- Timings using list for input data ---

%timeit get_input_list(path)
166 µs ± 347 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit p1(data)
1.62 ms ± 5.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit p2(data)
158 ms ± 863 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit faster_p1(data)
486 µs ± 1.36 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit faster_p2(data)
90.1 ms ± 254 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit Part1(data)
77.4 µs ± 161 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Part2(data)
12.5 ms ± 15.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
'''
