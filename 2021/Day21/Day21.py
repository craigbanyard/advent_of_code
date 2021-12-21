from helper import aoc_timer
from collections import Counter
from functools import cache
import itertools as it


P1_MAX = 1000
P2_MAX = 21
OUTCOMES = Counter([sum(d) for d in it.product(range(1, 4), repeat=3)])


@aoc_timer
def get_input(path):
    return [int(x[-1]) for x in open(path).read().splitlines()]


def deterministic_roll(pos1, pos2, score1, score2, turn):
    if score2 >= P1_MAX:
        return score1 * turn
    pos1 = (pos1 + (3 * turn + 6)) % 10 or 10
    score1 += pos1
    return deterministic_roll(pos2, pos1, score2, score1, turn + 3)


@cache
def quantum_roll(pos1, pos2, score1, score2):
    if score2 >= P2_MAX:
        return (0, 1)
    wins1 = wins2 = 0
    for outcome, freq in OUTCOMES.items():
        pos1_new = (pos1 + outcome) % 10 or 10
        score1_new = score1 + pos1_new
        win2, win1 = quantum_roll(pos2, pos1_new, score2, score1_new)
        wins1 += freq * win1
        wins2 += freq * win2
    return wins1, wins2


@aoc_timer
def Day21(data):
    args = (*data, 0, 0)
    p1 = deterministic_roll(*args, 0)
    p2 = max(quantum_roll(*args))
    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 21")
    data = get_input('input.txt')
    p1, p2 = Day21(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
