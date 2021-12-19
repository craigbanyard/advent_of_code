from helper import aoc_timer
from collections import Counter, defaultdict
import itertools as it
from matplotlib import pyplot as plt


@aoc_timer
def get_input(path):
    S = defaultdict(list)
    for idx, group in enumerate(open(path).read().split('\n\n')):
        _, *coords = group.splitlines()
        for c in coords:
            S[idx].append(tuple(map(int, c.split(','))))
    return S


def euc(a, b):
    return sum((p - q) ** 2 for p, q in zip(a, b))


@aoc_timer
def Day19(data: dict[int: list]):
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # colours = ['red', 'green', 'blue', 'orange', 'purple']

    # Relative Euclidean distances of each beacon from every other (by sensor)
    # i.e. D[s1] = [{d01, d02, d03, ...}, {d11, d12, d13, ...}]
    D, B = {}, {}
    for s, beacons in data.items():
        npoints = len(beacons)
        D[s] = [set() for _ in range(npoints)]
        B[s] = [{} for _ in range(npoints)]

        # xs, ys, zs = zip(*beacons)
        # ax.scatter(xs, ys, zs, color=colours[s])

        for i, j in it.product(range(npoints), range(npoints)):
            distance = euc(beacons[i], beacons[j])
            D[s][i].add(distance)
            B[s][i][distance] = beacons[j]

    M = defaultdict(set)
    R = {}
    for s1, s2 in it.combinations(D.keys(), 2):
        for i, j in it.product(range(len(D[s1])), range(len(D[s2]))):
            U = D[s1][i] & D[s2][j]
            if len(U) >= 12:
                for d in U:
                    M[(s1, B[s1][i][d])].add((s2, B[s2][j][d]))
                print(f'{s1} & {s2}: {U}, n = {len(U)}')
                R[(s1, s2)] = [Counter() for _ in range(3)]
                break

    overlaps = 0
    ROTS = {}  # TODO: Implement the rotations properly
    for k, v in M.items():
        print(f'{k} -> {v}')
        overlaps += len(v)
        s1, b1 = k
        for s2, b2 in v:
            for idx, orien in enumerate(it.permutations(b2)):
                for pos, (p, q) in enumerate(zip(b1, orien)):
                    R[(s1, s2)][pos][p - q] += 1
                    R[(s1, s2)][pos][p + q] += 1
                    val, count = R[(s1, s2)][pos].most_common()[0]
                    if count >= 12 and (s1, pos) not in ROTS:
                        ROTS[(s1, pos)] = (s2, idx, val)

    # for k, v in R.items():
    #     print(f'{k}: {[x.most_common()[0] for x in v]}')

    for k, v in ROTS.items():
        print(f'{k}: {v}')

    # Part 1: 346 is too low.
    # Part 1: 454 is too high.

    # plt.show()
    return sum(len(v) for _, v in data.items()) - overlaps, None


# %% Output
def main():
    print("AoC 2021\nDay 19")
    data = get_input('input.txt')
    data = get_input('sample.txt')
    # data = get_input('test1.txt')
    p1, p2 = Day19(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
