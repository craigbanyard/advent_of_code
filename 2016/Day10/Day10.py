from helper import aoc_timer
from collections import defaultdict, deque
from numpy import product


def to_int(x):
    try:
        return int(x)
    except ValueError:
        return x


@aoc_timer
def get_input(path):
    Q = deque()
    for line in open(path).read().splitlines():
        match list(map(to_int, line.split())):
            case ['value', m, *_, n]:
                Q.append(('value', m, n))
            case ['bot', m, _, _, _, d1, n1, *_, d2, n2]:
                Q.append((m, (d1, n1), (d2, n2)))
    return Q


@aoc_timer
def Day10(Q: deque, chips: tuple[int, int], bins: range):
    dest = {
        'bot': (bots := defaultdict(list)),
        'output': (outs := defaultdict(list))
    }
    while Q:
        match Q.popleft():
            case ('value', m, n):
                if len(bots[n]) == 2:
                    Q.append(('value', m, n))
                    continue
                bots[n].append(m)
            case (m, (d1, n1), (d2, n2)):
                if len(bots[m]) != 2:
                    Q.append((m, (d1, n1), (d2, n2)))
                    continue
                lo, hi = sorted(bots[m])
                if (lo, hi) == chips:
                    yield m
                chk1 = d1 == 'bot' and len(bots[n1]) == 2
                chk2 = d2 == 'bot' and len(bots[n2]) == 2
                if chk1 or chk2:
                    Q.append((m, (d1, n1), (d2, n2)))
                    continue
                dest[d1][n1].append(lo)
                dest[d2][n2].append(hi)
    yield product([outs[x][0] for x in bins])


# %% Output
def main():
    print("AoC 2016\nDay 10")
    data = get_input('input.txt')
    solver = Day10(Q=data, chips=(17, 61), bins=range(3))
    p1 = next(solver)
    p2 = next(solver)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
