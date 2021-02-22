from helper import aoc_timer


@aoc_timer
def get_input(path):
    for group in open(path).read().split('\n\n'):
        yield [set(person) for person in group.splitlines()]


@aoc_timer
def Day06(path):
    p1, p2 = 0, 0
    for group in get_input(path):
        p1 += len(set.union(*group))
        p2 += len(set.intersection(*group))
    return p1, p2


# %% Output
def main():
    print("AoC 2020\nDay 06")
    p1, p2 = Day06('input.txt')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 297 ns ± 3.3 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

# %timeit Day06('input.txt')
# 2.76 ms ± 20.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
