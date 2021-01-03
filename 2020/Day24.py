from helper import aoc_timer
from os import getcwd
from collections import defaultdict, Counter


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
    D = dirs()
    IN = []
    for line in open(path).read().split('\n'):
        instr, idx, end = 0, 0, len(line)
        while idx < end:        
            if (d := line[idx]) in D:
                instr += D[d]
                idx += 1
            elif (d := line[idx:idx+2]) in D:
                instr += D[d]
                idx += 2
        IN.append(instr)
    return IN


@aoc_timer
def Day24(data, part1=True):
    # Part 1
    IN = {k for k, v in Counter(data).items() if v % 2 != 0}
    if part1:
        return len(IN)

    # Part 2
    for t in range(100):
        S = defaultdict(int)
        for tile in IN:
            for d, n in dirs().items():
                S[tile + n] += 1
        # White tiles visited as adjacents
        W = {k for k, v in S.items() if v == 2 and k not in IN}
        # Black tiles visited as adjacents
        B = {a for a in IN & {k for k, v in S.items() if v <= 2}}
        # New state is union of W and B
        IN = W | B
    return len(IN)


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
3.73 ms ± 5.37 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit Day24(data)
136 µs ± 119 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day24(data, False)
629 ms ± 1.03 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
'''
