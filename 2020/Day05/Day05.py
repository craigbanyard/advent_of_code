from helper import aoc_timer


@aoc_timer
def get_input(path):
    return {int(s.translate(s.maketrans('FBLR', '0101')), 2)
            for s in open(path).readlines()}


@aoc_timer
def Day05(data, part1=True):
    for x in sorted(data, reverse=True):
        if part1:
            return x
        if x - 1 not in data and x - 2 in data:
            return x - 1


# %% Output
def main():
    print("AoC 2020\nDay 05")
    data = get_input('input.txt')
    print("Part 1:", Day05(data))
    print("Part 2:", Day05(data, False))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 869 µs ± 4.81 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit Day05(data, True)
# 11.5 µs ± 21 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

# %timeit Day05(data, False)
# 26 µs ± 412 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
