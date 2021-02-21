from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


# %% Functions for Part 1
def three_vowels(S):
    return sum(map(S.count, 'aeiou')) >= 3


def has_rep(S):
    return sum(a == b for a, b in zip(S, S[1:])) >= 1


def no_disallowed(S):
    disallowed = ['ab', 'cd', 'pq', 'xy']
    return sum(map(S.count, disallowed)) == 0


def nice_string(S):
    # Test one condition at a time - faster than all at once as some will not need to be evaluated
    if three_vowels(S):
        if has_rep(S):
            if no_disallowed(S):
                return True
    return False


# %% Functions for Part 2
def split_overlap(S, n):
    return [S[i:(i + n)] for i in range(len(S) - n + 1)]


def double_pair(S):
    pairs = split_overlap(S, 2)
    return sum(map(S.count, pairs)) > len(pairs)


def sandwich(S):
    triples = split_overlap(S, 3)
    for t in triples:
        if t[0] == t[-1]:
            return True
    return False


def nicer_string(S):
    # Test one condition at a time - faster than both at once as some will not need to be evaluated
    if double_pair(S):
        if sandwich(S):
            return True
    return False


# %% Driver
@aoc_timer
def Day05(data, part1=True):
    if part1:
        return sum(map(nice_string, data))
    return sum(map(nicer_string, data))


# %% Output
def main():
    print("AoC 2015\nDay 05")
    data = get_input('input.txt')
    print("Part 1:", Day05(data))
    print("Part 2:", Day05(data, part1=False))


if __name__ == '__main__':
    main()
