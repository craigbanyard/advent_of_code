from time import time
import re
from os import getcwd


def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def get_input(path):
    delims = [': ', '-', ' ']
    parse = lambda x: re_split(delims, x.strip())
    return [list(map(to_int, parse(x))) for x in open(path).readlines()]


def Day02(data):
    p1, p2 = 0, 0
    for lo, hi, x, pwd in data:
        if lo <= pwd.count(x) <= hi:
            p1 += 1
        if (pwd[lo-1] == x) ^ (pwd[hi-1] == x):
            p2 += 1
    return p1, p2


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day02.txt"
    print("AoC 2020\nDay 2\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    p1, p2 = Day02(data)
    print("Part 1:", p1)
    print("Part 2:", p2)
    print("Time:", time() - t0, "\n-----")


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
11 ms ± 243 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit Day02(data)
527 µs ± 4.18 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''
