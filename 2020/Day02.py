from helper import aoc_timer
from os import getcwd


@aoc_timer
def Day02(path):
    p1, p2 = 0, 0
    for line in open(path).read().split('\n'):
        rng, x, pwd = line.split()
        lo, hi = map(int, rng.split('-'))
        x = x[0]
        if lo <= pwd.count(x) <= hi:
            p1 += 1
        if (pwd[lo-1] == x) ^ (pwd[hi-1] == x):
            p2 += 1
    return p1, p2


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day02.txt"
    print("AoC 2020\nDay 2")
    p1, p2 = Day02(path)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()


'''
%timeit Day02(path)
1.55 ms ± 2.46 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''
