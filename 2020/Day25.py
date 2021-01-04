from helper import aoc_timer
from os import getcwd


@aoc_timer
def get_input(path):
    return {int(x.strip()) for x in open(path).readlines()}


@aoc_timer
def Day25(data, g, p):
    a, n = 1, 1
    while n < p:
        a = (a * g) % p
        if a in data:
            b = (data ^ {a}).pop()
            return pow(b, n, p)
        n += 1


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day25.txt"
    data = get_input(path)
    print("Day 25:", Day25(data, 7, 20201227))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
101 µs ± 78.8 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day25(data, 7, 20201227)
165 ms ± 2.66 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
'''
