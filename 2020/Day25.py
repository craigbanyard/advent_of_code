from helper import aoc_timer
from os import getcwd


@aoc_timer
def get_input(path):
    return {int(x.strip()) for x in open(path).readlines()}


@aoc_timer
def Day25(data):
    # Public base and modulus
    g, p = 7, 20201227
    # Private keys
    a, b = False, False
    # Starting point
    c, d = 1, 1
    while not (a and b):
        c = (c * g) % p
        if c in data:
            if a:
                return pow(c, a, p)
            a = d
        d += 1


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day25.txt"
    # data = {5764801, 17807724}
    data = get_input(path)
    print("Day 25:", Day25(data))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
102 µs ± 2.41 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day25(data)
1.94 s ± 2.17 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
'''
