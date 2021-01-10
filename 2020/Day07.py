from helper import aoc_timer
import re
from collections import deque, defaultdict
from os import getcwd


# Returns two dictionaries:
#     C = children - contents of each bag, including numbers (part 2)
#     P = parents - parents of each bag, excluding numbers (part 1)
@aoc_timer
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
@aoc_timer
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
@aoc_timer
def p2(C, target, time=True):
    cnt = 1
    for inner in C[target]:
        n, bag = inner
        cnt += n * p2(C, bag, time=False)
    return cnt


# %% Output
def main():
    print("AoC 2020\nDay 7")
    path = getcwd() + "\\Inputs\\Day07.txt"
    C, P = get_input(path)
    target = 'shiny gold'
    print("Part 1:", p1(P, target))
    print("Part 2:", p2(C, target) - 1)


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
