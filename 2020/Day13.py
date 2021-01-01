from time import time
from os import getcwd
from math import gcd


def get_input(path):
    lines = [x.strip() for x in open(path).readlines()]
    dep = int(lines[0])
    busses = lines[1].split(',')
    offsets = {int(bus): idx for idx, bus in enumerate(busses) if bus != 'x'}
    return dep, offsets


def lcm(a, b):
    return (a*b)//gcd(a, b)


def part1(dep, offsets):
    best = 1e12
    for bus in offsets.keys():
        wait = bus - dep % bus
        if wait < best:
            best = wait
            ans = best * bus
    return ans


def part2(offsets):
    t = 0
    tstep = list(offsets.keys())[0]
    for bus, off in offsets.items():
        while True:
            if (t + off) % bus == 0:
                tstep = lcm(tstep, bus)
                break
            t += tstep
    return t


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day13.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day13.txt"
    print("AoC 2020\nDay 13\n-----")
    t0 = time()
    dep, offsets = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    print("Part 1:", part1(dep, offsets))
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    print("Part 2:", part2(offsets))
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
124 µs ± 220 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit part1(dep, offsets)
1.02 µs ± 1.94 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

%timeit part2(offsets)
80.3 µs ± 103 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
'''
