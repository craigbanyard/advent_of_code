from helper import aoc_timer
from collections import defaultdict


@aoc_timer
def get_input(path):
    # Index 0 is for part 1, read horizontally
    # Indices 1:3 are for part 2, read vertically
    T = [defaultdict(list) for _ in range(4)]
    for idx, line in enumerate(open(path).readlines()):
        tri = list(map(int, line.split()))
        T[0][idx] = tri
        j = idx // 3
        for i, side in enumerate(tri, start=1):
            T[i][j].append(side)
    return T


@aoc_timer
def Day03(data):
    possible = [0 for _ in range(4)]
    for idx, triangles in enumerate(data):
        for _, triangle in triangles.items():
            triangle.sort()
            a, b, c = triangle
            if c < (a + b):
                possible[idx] += 1
    p1, *p2 = possible
    return p1, sum(p2)


# %% Output
def main():
    print("AoC 2016\nDay 03")
    data = get_input('input.txt')
    p1, p2 = Day03(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
