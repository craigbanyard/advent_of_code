from helper import aoc_timer
from os import getcwd


@aoc_timer
def get_input(path):
    return [(x[0], int(x[1:])) for x in open(path).read().split('\n')]


def rotate(c, d, u):
    clock = ['N', 'E', 'S', 'W']
    turn = {'L': -u//90, 'R': u//90}
    return clock[(clock.index(c) + turn[d]) % 4]


def rotate_w(w, d, u):
    # Reduce to (x, y) = (E, N)
    w['N'] -= w['S']
    w['E'] -= w['W']
    w['S'] = w['W'] = 0
    turn = {'L': -u//90, 'R': u//90}
    for _ in range(turn[d] % 4):
        w['E'], w['N'] = w['N'], -w['E']
    return w


@aoc_timer
def Day12(data, part1=True):

    # Relevant for both parts:
    rots = {'L', 'R'}
    dirs = {k: 0 for k in 'NESW'}

    if part1:
        curr = 'E'
        for head, unit in data:
            if head in rots:
                curr = rotate(curr, head, unit)
                continue
            if head == 'F':
                dirs[curr] += unit
                continue
            dirs[head] += unit
    else:
        wayp = {'N': 1, 'E': 10, 'S': 0, 'W': 0}
        for head, unit in data:
            if head in rots:
                wayp = rotate_w(wayp, head, unit)
                continue
            if head == 'F':
                for h in wayp:
                    dirs[h] += unit * wayp[h]
                continue
            wayp[head] += unit

    # Both parts have same return calculation
    return abs(dirs['N'] - dirs['S']) + abs(dirs['W'] - dirs['E'])


# %% Output
def main():
    print("AoC 2020\nDay 12")
    path = getcwd() + "\\Inputs\\Day12.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day12.txt"
    data = get_input(path)
    print("Part 1:", Day12(data))
    print("Part 2:", Day12(data, False))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
389 µs ± 377 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day12(data)
217 µs ± 675 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day12(data, False)
567 µs ± 1.18 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''
