from time import time
from os import getcwd
from collections import deque


def get_input(path):
    return [int(x.strip()) for x in open(path).readlines()]


def part1(data, pre):
    for idx, x in enumerate(data[pre:]):
        valid = False
        prior = data[idx:idx+pre]
        for y in prior:
            if x - y in prior:
                valid = True
                break
        if not valid:
            return x


def part2(data, target):
    n = 2
    while True:
        for idx, x in enumerate(data):
            rng = data[idx:idx+n]
            if sum(rng) == target:
                return min(rng) + max(rng)
        n += 1


def part1_alt(data, pre=25):
    STACK = deque(data[:pre], maxlen=pre)
    for x in data[pre:]:
        found = False
        for y in STACK:
            if x - y in STACK:
                found = True
                break
        if not found:
            return x
        STACK.append(x)


def part2_alt(data, target):
    Q = deque()
    rsum = 0
    for x in data:
        if rsum < target:
            rsum += x
            Q.append(x)
        while rsum > target:
            rsum -= Q.popleft()
        if rsum == target:
            return min(Q) + max(Q)


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day09.txt"
    print("AoC 2020\nDay 9\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    p1 = part1(data, 25)
    print("Part 1:", p1)
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    p2 = part2(data, p1)
    print("Part 2:", p2)
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit part1(data, 25)
896 µs ± 5.19 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit part1_alt(data, 25)
936 µs ± 2.02 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit part2(data, p1)
7.23 ms ± 12.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit part2_alt(data, p1)
164 µs ± 396 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
'''
