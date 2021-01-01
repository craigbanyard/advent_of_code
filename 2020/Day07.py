from time import time
import re
from functools import reduce
from collections import deque, defaultdict
from os import getcwd


# Returns two dictionaries:
#     C = children - contents of each bag, including numbers (part 2)
#     P = parents - parents of each bag, excluding numbers (part 1)
def get_input(path):
    C, P = defaultdict(list), defaultdict(list)
    for line in open(path).readlines():
        bag, contents = line.split(' bags contain ')
        items = re.findall(r'(\d+) ([^,]+) bag', contents)
        for n, inner in items:
            C[bag].append((int(n), inner))
            P[inner].append(bag)
    return C, P


# Part 1 - BFS
def p1(P, target):
    SEEN = set()
    Q = deque([target])
    while Q:
        x = Q.popleft()
        if x in SEEN:
            continue
        SEEN.add(x)
        if x not in P:
            # Edge of graph - bag has no parents
            continue
        for y in P[x]:
            Q.append(y)
    return len(SEEN) - 1


# Part 2 - RECURSION
# Returns 1 higher than number of bags contained in target (i.e. includes target)
def p2(C, target):
    cnt = 1
    for inner in C[target]:
        n, bag = inner
        cnt += n * p2(C, bag)
    return cnt


# %% Original Part 1 - 3 seconds - slow!


def multi_replace(repls, string):
    return reduce(lambda a, kv: a.replace(*kv), repls, string)


def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


# Return dictionary of parent: children
def get_input_orig(path):
    delims = [' contain ', ', ']
    repls = (' bags', ''), (' bag', ''), ('no other', '0 other')
    parse = lambda x: re_split(delims, multi_replace(repls, x).strip('.\n'))
    return {k: v for k, *v in [parse(x) for x in open(path).readlines()]}


def p1_driver(data, target):
    def p1_orig(data, outer, target):
        cnt = 0
        for inner in data[outer]:
            n, bag = list(map(to_int, inner.split(' ', 1)))
            if bag == 'other':
                return 0
            if bag == target:
                return 1
            cnt = max(cnt, p1_orig(data, bag, target))
        return cnt

    cnt = 0
    for outer in data.keys():
        cnt += p1_orig(data, outer, target)
    return cnt


def p2_orig(data, target):
    cnt = 1
    for inner in data[target]:
        n, bag = list(map(to_int, inner.split(' ', 1)))
        if bag == 'other':
            return cnt
        cnt += n * p2_orig(data, bag)
    return cnt


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day07.txt"
    print("AoC 2020\nDay 7\n-----")
    t0 = time()
    C, P = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    target = 'shiny gold'
    print("Part 1:", p1(P, target))
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    print("Part 2:", p2(C, target) - 1)
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
3.41 ms ± 102 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit p1(P,target)
42.1 µs ± 138 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit p2(C,target)
20.1 µs ± 67.9 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
'''
