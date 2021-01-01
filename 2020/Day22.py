from helper import aoc_timer
from os import getcwd
from collections import defaultdict, deque
from itertools import islice
from copy import deepcopy


@aoc_timer
def get_input(path):
    D = defaultdict(deque)
    for line in open(path).read().split('\n'):
        if 'Player' in line:
            n = int(line[-2])
            continue
        if line:
            D[n].append(int(line))
    return D


def score(deck):
    return sum(idx * c for idx, c in enumerate(reversed(deck), start=1))


def state(D):
    return tuple(score(d) for d in D.values())


def new_game(turn, D, part2):
    if not part2:
        return False
    return all(c <= len(d) for c, d in zip(turn, D.values()))


def new_decks(D, cards):
    return {p: deque(islice(D[p], 0, c)) for p, c in zip(D.keys(), cards)}


def recursive_combat(D, part2=True, output=False):
    if part2:
        SEEN = {state(D)}
    if output:
        t, games = 0, 0
    while D[1] and D[2]:
        turn = [D[x].popleft() for x in D]
        if new_game(turn, D, part2):
            if output:
                print(f"{'=' * 5} Recursing {'=' * 5}")
            newD = new_decks(D, turn)
            _, winner = recursive_combat(newD)
            D[winner].extend(turn if winner == 1 else turn[::-1])
            if output:
                print(f"{'=' * 5} Back up one level {'=' * 5}")
                print(f"Round: {len(SEEN) + games}, Winner: {winner}, D1: {D[1]}, D2: {D[2]}")
                games += 1
            continue
        winner = 2 - (turn[0] > turn[1])
        D[winner].extend(sorted(turn, reverse=True))
        if output and not part2:
            t += 1
            print(f"Round: {t}, Winner: {winner}, D1: {D[1]}, D2: {D[2]}")
        if part2:
            if output:
                print(f"Round: {len(SEEN) + games}, Winner: {winner}, D1: {D[1]}, D2: {D[2]}")
            s = state(D)
            if s in SEEN:
                break
            SEEN.add(s)
    win_deck = D[1] or D[2]
    winner = 2 - (win_deck == D[1])
    return score(win_deck), winner


@aoc_timer
def Day22(data, part2=False, output=False):
    D = deepcopy(data)
    return recursive_combat(D, part2, output)


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day22.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day22.txt"
    print("AoC 2020\nDay 22")
    data = get_input(path)
    print("Part 1:", Day22(data, part2=False, output=False))
    print("Part 2:", Day22(data, part2=True, output=False))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
110 µs ± 319 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit Day22(data, False, False)
513 µs ± 562 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day22(data, True, False)
3.59 s ± 133 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
'''
