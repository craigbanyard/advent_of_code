from helper import aoc_timer


@aoc_timer
def get_input(data, mod):
    cups = [None] * ((mx := len(data)) + 1)
    last = int(data[-1])
    for idx, cup in enumerate(data, start=1):
        cups[int(cup)] = int(data[idx % mx])
    if mod > mx:
        cups[last] = (mx := mx + 1)
        cups += list(range(mx + 1, mod + 1)) + [int(data[0])]
    return cups


def dec_mod(n, m):
    return n - 1 or m


def turn(cup, cups, mod):
    dest = dec_mod(cup, mod)
    p1 = cups[cup]
    p2 = cups[p1]
    p3 = cups[p2]
    while dest == p1 or dest == p2 or dest == p3:
        dest = dec_mod(dest, mod)
    return p1, p3, cups[p3], dest, cups[dest]


def p1(cups, cup=1, mod=9):
    ans = ''
    for _ in range(mod - 1):
        ans += str((cup := cups[cup]))
    return ans


@aoc_timer
def Day23(data, mod=9, moves=100, part1=True):
    cups = get_input(data, mod)
    cup = int(data[0])
    for m in range(moves):
        p, q, ncup, a, b = turn(cup, cups, mod)
        cups[cup] = ncup
        cups[a] = p
        cups[q] = b
        cup = ncup
    if part1:
        return p1(cups)
    return (a := cups[1]) * cups[a]


# %% Output
def main():
    data = '589174263'
    print("AoC 2020\nDay 23")
    print("Part 1:", Day23(data))
    print("Part 2:", Day23(data, 1000000, 10000000, False))


if __name__ == '__main__':
    main()


'''
%timeit Day23(data)
85.3 µs ± 78.2 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
'''
