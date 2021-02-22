from helper import aoc_timer


@aoc_timer
def get_input(path):
    for line in open(path).read().split('\n'):
        rng, x, pwd = line.split()
        lo, hi = map(int, rng.split('-'))
        yield lo, hi, x[0], pwd


@aoc_timer
def Day02(path):
    p1, p2 = 0, 0
    for lo, hi, x, pwd in get_input(path):
        if lo <= pwd.count(x) <= hi:
            p1 += 1
        if (pwd[lo - 1] == x) ^ (pwd[hi - 1] == x):
            p2 += 1
    return p1, p2


# %% Output
def main():
    print("AoC 2020\nDay 02")
    p1, p2 = Day02('input.txt')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 262 ns ± 0.417 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

# %timeit Day02('input.txt')
# 1.55 ms ± 2.46 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
