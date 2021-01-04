from helper import aoc_timer
from os import getcwd
from collections import defaultdict


def dirs():
    # Use complex numbers to represent hexagonal grid
    return {
        'e': 1,
        'ne': 0.5+1j,
        'nw': -0.5+1j,
        'w': -1,
        'sw': -0.5-1j,
        'se': 0.5-1j
        }


@aoc_timer
def get_input(path):
    D, IN = dirs(), set()
    for line in open(path).read().split('\n'):
        instr, idx, end = 0, 0, len(line)
        while idx < end:        
            if (d := line[idx]) in D:
                idx += 1
            elif (d := line[idx:idx+2]) in D:
                idx += 2
            instr += D[d]
        IN ^= {instr}
    return IN


@aoc_timer
def Day24(data, part1=True):
    # Part 1
    if part1:
        return len(data)

    # Part 2
    for t in range(100):
        S = defaultdict(int)
        for tile in data:
            for d, n in dirs().items():
                S[tile + n] += 1
        # White tiles visited as adjacents
        W = {k for k, v in S.items() if v == 2 and k not in data}
        # Black tiles visited as adjacents
        B = {a for a in data & {k for k, v in S.items() if v <= 2}}
        # New state is union of W and B
        data = W | B
    return len(data)


# %% Output
def main():
    print("AoC 2020\nDay 24")
    path = getcwd() + "\\Inputs\\Day24.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day24.txt"
    data = get_input(path)
    print("Part 1:", Day24(data))
    print("Part 2:", Day24(data, False))



if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
3.86 ms ± 6.71 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit Day24(data)
246 ns ± 0.524 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

%timeit Day24(data, False)
627 ms ± 930 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
'''
