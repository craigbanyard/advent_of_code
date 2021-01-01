from time import time, sleep
from os import getcwd


def get_input(path):
    return [x.strip() for x in open(path).readlines()]


# %% Final code: process trajectory and map at the same time
def Day03(data, slopes):
    rows, cols = len(data), len(data[0])
    prod = 1
    for dr, dc in slopes:
        c, collisions = 0, 0
        for r in range(dr, rows, dr):
            c = (c + dc) % cols
            if data[r][c] == '#':
                collisions += 1
        prod *= collisions
    return collisions, prod


# %% Visualisation code
def Day03_vis(data, slopes):
    rows, cols = len(data), len(data[0])
    for dr, dc in slopes:
        c, collisions = 0, 0
        print(data[0])
        for r in range(dr, rows, dr):
            c = (c + dc) % cols
            line = data[r][:c]
            if data[r][c] == '#':
                collisions += 1
                line += 'X' + data[r][c+1:] + '    Ouch: ' + str(collisions)
            else:
                line += 'O' + data[r][c+1:]
            print(line)
            sleep(0.05)


# %% Original code
def get_trees(data, tree):
    rows, cols, trees = len(data), len(data[0]), set()
    [trees.add((r, c)) for r in range(rows) for c in range(cols) if data[r][c] == tree]
    return trees, rows, cols


def Day03_orig(data, slopes):
    # Process trees
    trees, rows, cols = get_trees(data,'#')
    # Check trajectories
    prod = 1
    for dr, dc in slopes:
        r, c, collisions = 0, 0, 0
        for row in range(rows):
            r += dr
            c = (c + dc) % cols
            if (r, c) in trees:
                collisions += 1
        prod *= collisions
    return collisions, prod


# %% Alternative: set of trajectories, intersect with set of trees
def Day03_alt(data,slopes):
    # Process trees
    trees,rows,cols = get_trees(data,'#')
    # Check trajectories
    prod = 1
    for dr,dc in slopes:
        c, traj = 0,set()
        c = 0
        for r in range(0,rows,dr):
            c = (c + dc) % cols
            traj.add((r+dr, c))
        collisions = len(traj.intersection(trees))
        prod *= collisions
    return collisions, prod


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day03.txt"
    print("AoC 2020\nDay 3\n-----")
    t0 = time()
    data = get_input(path)
    slopes1, slopes2 = [(1, 3)], [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    p1, _ = Day03(data, slopes1)
    print("Part 1:", p1)
    print("Time:", time() - t0, "\n-----")
    t0 = time()
    _, p2 = Day03(data, slopes2)
    print("Part 2:", p2)
    print("Time:", time() - t0, "\n-----")


if __name__ == '__main__':
    main()


''' NEED TO REDO TIMINGS

'''
