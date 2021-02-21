from helper import aoc_timer
from itertools import groupby


def get_next(n):
    """Iteratively generate the sequence."""
    n = str(n)
    look, counter, say = n[0], 1, ''
    for d in n[1:]:
        if look == d:
            counter += 1
            continue
        say += str(counter) + look
        counter = 1
        look = d
    return say + str(counter) + look


def look_and_say(seed):
    """One-liner using itertools.groupby - slower than iterative approach."""
    return ''.join([(str(len([1 for _ in g])) + k) for k, g in groupby(seed)])


@aoc_timer
def Day10(seed, steps):
    for _ in range(steps):
        # Fast but ugly
        seed = get_next(seed)
        # Sexy but slow
        # seed = look_and_say(seed)
    return seed


# %% Output
def main():
    print("AoC 2015\nDay 10")
    seed = '1113122113'
    p1 = Day10(seed, 40)
    print("Part 1:", len(p1))
    print("Part 2:", len(Day10(p1, 10)))


if __name__ == '__main__':
    main()
