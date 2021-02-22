from helper import aoc_timer
from collections import deque


@aoc_timer
def get_input(path):
    return [int(x.strip()) for x in open(path).readlines()]


@aoc_timer
def part1(data, pre):
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


@aoc_timer
def part2(data, target):
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
    print("AoC 2020\nDay 09")
    data = get_input('input.txt')
    p1 = part1(data, 25)
    print("Part 1:", p1)
    print("Part 2:", part2(data, p1))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 461 µs ± 419 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit part1(data, 25)
# 898 µs ± 884 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit part2(data, p1)
# 171 µs ± 275 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
