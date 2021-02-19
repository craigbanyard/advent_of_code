from helper import aoc_timer
import re


def re_split(delimiters, string):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string)


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def parse(x, delims):
    return list(map(to_int, re_split(delims, x.strip('seconds.\n'))))


@aoc_timer
def get_input(path):
    delims = [' can fly ', ' km/s for ', ' seconds, but then must rest for ']
    return [list(map(to_int, parse(x, delims))) for x in open(path).readlines()]


def get_pos(data, t):
    R = {}
    for r, speed, dur, rest in data:
        R[r] = (t // (dur + rest) * dur + min(t % (dur + rest), dur)) * speed
    return [(k, v) for k, v in R.items() if v == max(R.values())]


@aoc_timer
def Day14(data, part1=True):
    t = 2503
    if part1:
        return get_pos(data, t)

    # Part 2
    P = {}
    for t in range(2503):
        for r, p in get_pos(data, t+1):
            if r not in P:
                P[r] = 1
                continue
            P[r] += 1

    return [(k, v) for k, v in P.items() if v == max(P.values())]


# %% Output
def main():
    print("AoC 2015\nDay 15")
    data = get_input('input.txt')
    print("Part 1:", Day14(data))
    print("Part 2:", Day14(data, part1=False))


if __name__ == '__main__':
    main()
