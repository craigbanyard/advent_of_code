from helper import aoc_timer
import re
from itertools import permutations, combinations


def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def parse(x, delims):
    return list(map(to_int, re_split(delims, x.replace('would lose ', '-').strip('.\n'))))


@aoc_timer
def get_input(path):
    delims = [' would gain ', ' happiness units by sitting next to ', ' ']
    return [list(map(to_int, parse(x, delims))) for x in open(path).readlines()]


# Function used to discard arrangements that are the reverse of other arrangements
# This halves the number of permutations (iterations) required to find max happiness
def get_unique_perms(guests):
    for g in permutations(guests):
        if g <= g[::-1]:
            yield g


@aoc_timer
def Day13(h, part1=True):
    # Get unique guests
    G = set(a for a, b, n in h)

    # Create dictionary of net happiness gain from two adjacent guests
    H_temp, H = {}, {}
    for g1, n, g2 in h:
        H_temp[(g1, g2)] = n

    # Add both directional arrangements to save check later
    for g1, g2 in combinations(G, 2):
        H[(g1, g2)] = H[(g2, g1)] = H_temp[(g1, g2)] + H_temp[(g2, g1)]

    # Part 1: Fix table position of one guest and generate permutations of the rest
    # Part 2: Assume fixed guest is myself and everyone is ambivalent about sitting next to me
    g = G.copy()
    if part1:
        fix = h[-1][0]
        g.remove(fix)

    # Cycle permutations and return happiest arrangement
    happiest = 0
    for arr in get_unique_perms(g):
        # Add net happiness gain from fixed guest (zero if this is myself - part 2)
        if part1:
            net = H[(fix, arr[0])] + H[(arr[-1], fix)]
        else:
            net = 0
        for g1, g2 in zip(arr, arr[1:]):
            net += H[(g1, g2)]
        happiest = max(happiest, net)

    return happiest


# %% Output
def main():
    print("AoC 2015\nDay 15")
    data = get_input('input.txt')
    print("Part 1:", Day13(data))
    print("Part 2:", Day13(data, part1=False))


if __name__ == '__main__':
    main()
