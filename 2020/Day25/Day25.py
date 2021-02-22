from helper import aoc_timer
from math import ceil
from sympy.ntheory.residue_ntheory import discrete_log


@aoc_timer
def get_input(path):
    return {int(x.strip()) for x in open(path).readlines()}


@aoc_timer
def Day25(data, g, p):
    """Brute-force to first match."""
    a, n = 1, 1
    while n < p:
        a = (a * g) % p
        if a in data:
            b = (data ^ {a}).pop()
            return pow(b, n, p)
        n += 1
    return


@aoc_timer
def bsgs(data, g, p):
    """Baby-step giant-step on reversed data."""
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
def handshake(data, g, p):
    """SymPy discrete_log on raw data."""
    a, b = data
    x = discrete_log(p, a, g)
    return pow(b, x, p)


# %% Output
def main():
    print("AoC 2020\nDay 25")
    data = get_input('input.txt')
    g, p = 7, 20201227
    print("Brute:", Day25(data, g, p))
    print("BSGS:", bsgs(data, g, p))
    print("SymPy:", handshake(data, g, p))


if __name__ == '__main__':
    main()


# %timeit get_input('input.txt')
# 101 µs ± 78.8 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

# %timeit Day25(data, 7, 20201227)
# 165 ms ± 2.66 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

# %timeit bsgs(data, g, p)
# 838 µs ± 4.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

# %timeit handshake(data, g, p)
# 573 µs ± 2.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
