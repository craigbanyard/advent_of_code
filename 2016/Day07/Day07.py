from helper import aoc_timer
import re


IP = re.compile(r'\[([^\]]+)\]')


@aoc_timer
def get_input(path):
    for line in open(path).read().split():
        # Works even for adjacent hypernet sequences
        seq = re.split(IP, line)
        sup = ' '.join(seq[::2])
        hyp = ' '.join(seq[1::2])
        yield sup, hyp


def abba(s):
    return any(a == d and b == c and a != b and a != ' ' and b != ' '
               for a, b, c, d in zip(s, s[1:], s[2:], s[3:]))


def supports_tls(sup, hyp):
    return abba(sup) and not abba(hyp)


def supports_ssl(sup, hyp):
    return any(a == c and a != b and b + a + b in hyp and a != ' ' and b != ' '
               for a, b, c in zip(sup, sup[1:], sup[2:]))


@aoc_timer
def Day07(data):
    p1, p2 = 0, 0
    for sup, hyp in data:
        p1 += supports_tls(sup, hyp)
        p2 += supports_ssl(sup, hyp)
    return p1, p2


# %% Output
def main():
    print("AoC 2016\nDay 07")
    data = get_input('input.txt')
    p1, p2 = Day07(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
