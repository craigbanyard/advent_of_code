from helper import aoc_timer
from os import getcwd
from math import ceil
from sympy.ntheory.residue_ntheory import discrete_log


@aoc_timer
def get_input(path):
    return {int(x.strip()) for x in open(path).readlines()}


@aoc_timer
# Brute-force to first match
def Day25(data, g, p):
    a, n = 1, 1
    while n < p:
        a = (a * g) % p
        if a in data:
            b = (data ^ {a}).pop()
            return pow(b, n, p)
        n += 1
    return


@aoc_timer
# Baby-step giant-step on reversed data
def bsgs(data, g, p):
    b, a = data
    m = ceil(p ** 0.5)
    D, e = {}, 1
    for j in range(m):
        D[e] = j
        e = (e * g) % p
    g = pow(g, -m, p)
    e = a
    for i in range(m):
        if e in D:
            x = i * m + D[e]
            return pow(b, x, p)
        e = (e * g) % p
    return


@aoc_timer
# SymPy discrete_log on raw data
def handshake(data, g, p):
    a, b = data
    x = discrete_log(p, a, g)
    return pow(b, x, p)


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day25.txt"
    data = get_input(path)
    g, p = 7, 20201227
    print("Brute:", Day25(data, g, p))
    print("BSGS:", bsgs(data, g, p))
    print("SymPy:", handshake(data, g, p))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
101 µs ± 78.8 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day25(data, 7, 20201227)
165 ms ± 2.66 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit bsgs(data, g, p)
838 µs ± 4.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit handshake(data, g, p)
573 µs ± 2.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''
