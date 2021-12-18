from helper import aoc_timer
from collections import Counter, defaultdict
import itertools as it


@aoc_timer
def get_input(path):
    template, rules = open(path).read().split('\n\n')
    rules = {a: b for a, b in [line.split(' -> ') for line in rules.splitlines()]}
    return template, rules


@aoc_timer
def Day14(data, steps=10):
    template, rules = data
    C = Counter(template)
    P = Counter([a + b for a, b in it.pairwise(template)])
    for _ in range(steps):
        Q = defaultdict(int)
        for elem in P:
            a, c = elem
            b = rules[elem]
            n = P[elem]
            C[b] += n
            Q[a + b] += n
            Q[b + c] += n
        P = Q
    (_, m), *_, (_, n) = C.most_common()
    return m - n


# %% Output
def main():
    print("AoC 2021\nDay 14")
    data = get_input('input.txt')
    print("Part 1:", Day14(data, steps=10))
    print("Part 2:", Day14(data, steps=40))


if __name__ == '__main__':
    main()
