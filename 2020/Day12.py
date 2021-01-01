from time import time
from os import getcwd


def get_input(path):
    return [(y[0], int(y[1:])) for y in [x.strip() for x in open(path).readlines()]]


def rotate(c, d, u):
    clock = ['N', 'E', 'S', 'W']
    turn = {'L': -u//90, 'R': u//90}
    return clock[(clock.index(c) + turn[d]) % 4]


def Day12(data, part=1):

    # Dictionaries relevant for both parts
    rots = {'L', 'R'}
    dirs = {k: 0 for k in 'NSEW'}

    def part1():
        curr = 'E'
        for head, unit in data:
            if head in rots:
                curr = rotate(curr, head, unit)
                continue
            if head == 'F':
                dirs[curr] += unit
                continue
            dirs[head] += unit
        return abs(dirs['N'] - dirs['S']) + abs(dirs['W'] - dirs['E'])

    def part2():
        wayp = {'N': 1, 'S': 0, 'E': 10, 'W': 0}
        for head, unit in data:
            if head in rots:
                new = {k: 0 for k in 'NSEW'}
                for h in wayp:
                    new[rotate(h, head, unit)] = wayp[h]
                wayp = new
                continue
            if head == 'F':
                for h in wayp:
                    dirs[h] += unit * wayp[h]
                continue
            wayp[head] += unit
        return abs(dirs['N'] - dirs['S']) + abs(dirs['W'] - dirs['E'])

    if part == 2:
        return part2()
    return part1()


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day12.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day12.txt"
    print("AoC 2020\nDay 12\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    print("Part 1:", Day12(data))
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    print("Part 2:", Day12(data, part=2))
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
555 µs ± 3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day12(data)
217 µs ± 675 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day12(data,2)
864 µs ± 2.84 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
'''
