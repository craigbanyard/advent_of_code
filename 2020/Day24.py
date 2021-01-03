from helper import aoc_timer
from os import getcwd
from collections import defaultdict


def reduce_inv(instr):
    INV = {
        'e': 'w',
        'se': 'nw',
        'sw': 'ne'
        }
    new = defaultdict(int)
    for d, inv in INV.items():
        if d in instr:
            if inv in instr:
                if (n := instr[d] - instr[inv]) == 0:
                    continue
                elif n > 0:
                    new[d] = n
                else:
                    new[inv] = -n
            else:
                new[d] = instr[d]
        elif inv in instr:
            new[inv] = instr[inv]
    return new


def reduce_add(instr):
    ADD = {
        'e': ('ne', 'se'),
        'se': ('e', 'sw'),
        'sw': ('w', 'se'),
        'w': ('nw', 'sw'),
        'nw': ('w', 'ne'),
        'ne': ('e', 'nw')
        }
    for a, (b, c) in ADD.items():
        if b in instr and c in instr:
            if (n := instr[b]) == (m := instr[c]):
                instr[a] += n
                del instr[b], instr[c]
            elif n > m:
                instr[a] += m
                instr[b] = n - m
                del instr[c]
            elif m > n:
                instr[a] += n
                instr[c] = m - n
                del instr[b]
    return instr


def reduce(instr):
    instr = reduce_add(reduce_inv(instr))
    if len(instr) < 2:
        return instr
    if len(instr) == 2:
        return reduce_add(reduce_inv(instr))
    return reduce(instr)


@aoc_timer
def get_input(path):
    D = {'e', 'se', 'sw', 'w', 'nw', 'ne'}
    IN = []
    for line in open(path).read().split('\n'):
        idx = 0
        end = len(line)
        instr = defaultdict(int)
        while idx < end:        
            if (d := line[idx]) in D:
                instr[d] += 1
                idx += 1
            elif (d := line[idx:idx+2]) in D:
                instr[d] += 1
                idx += 2
        IN.append(tuple(sorted(reduce(instr).items())))
    return IN


def adjacent(tile):
    D = {'e', 'se', 'sw', 'w', 'nw', 'ne'}
    curr, N = defaultdict(int), []
    for d, n in tile:
        curr[d] += n
    for d in D:
        tmp = curr.copy()
        tmp[d] += 1
        N.append(tuple(sorted(reduce(tmp).items())))
    return N


@aoc_timer
def Day24(data, part1=True):
    # Part 1
    IN = defaultdict(int)
    for line in data:
        IN[line] += 1
        if IN[line] % 2 == 0:
            del IN[line]
    IN = set(IN.keys())
    if part1:
        return len(IN)

    # Part 2
    for t in range(100):
        S = defaultdict(int)
        for tile in IN:
            for a in adjacent(tile):
                S[a] += 1
        # White tiles visited as adjacents
        W = {k for k, v in S.items() if v == 2 and k not in IN}
        # Black tiles visited as adjacents
        B = {a for a in IN & {k for k, v in S.items() if v <= 2}}
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

'''
