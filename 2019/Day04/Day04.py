from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [int(x) for x in open(path).read().split('-')]


def get_digits(n):
    return list(map(int, str(n)))


def non_dec(N):
    return all(x <= y for x, y in zip(N, N[1:]))


def has_rep(N):
    return len(N) != len(set(N))


def valid2(N):
    uniques = set(N)
    for n in uniques:
        if N.count(n) == 2:
            return True
    return False


@aoc_timer
def Day04(data):
    p1, p2 = 0, 0
    for i in range(*data):
        N = get_digits(i)
        if non_dec(N) and has_rep(N):
            p1 += 1
            if valid2(N):
                p2 += 1
    return p1, p2


# %% Output
def main():
    print("AoC 2019\nDay 04")
    data = get_input('input.txt')
    p1, p2 = Day04(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
