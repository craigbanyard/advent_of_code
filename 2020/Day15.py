from time import time
from os import getcwd


def get_input(path):
    return [int(x) for x in open(path).read().split(',')]


def Day15(data, turns=2020, progress=False):
    # Initialise dictionary of last turn each number has been said
    said = {}
    for idx, val in enumerate(data):
        said[val] = idx + 1
    last = val
    # Play the game
    for t in range(len(data), turns):
        if last in said:
            nxt = t - said[last]
        else:
            nxt = 0
        said[last] = t
        last = nxt
        # Progress reporting
        if progress:
            if t % 1000000 == 0:
                print('.', end='', flush=True)
    if progress:
        print()
    return last


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day15.txt"
    print("AoC 2020\nDay 15\n-----")
    t0 = time()
    data = get_input(path)
    print("Data:", time() - t0, "\n-----")
    t0 = time()
    print("Part 1:", Day15(data))
    print("Time:", time() - t0, '\n-----')
    t0 = time()
    print("Part 2:", Day15(data, turns=30000000, progress=True))
    print("Time:", time() - t0)


if __name__ == '__main__':
    main()


# %% Old code:


def Day15_orig(data, turns=2020, progress=False):
    # Initialise dictionary of last two times each number has been said
    said = {}
    for idx, val in enumerate(data):
        said[val] = (idx, idx)
    last = val
    # Play the game
    for t in range(len(data), turns):
        t1, t2 = said[last]
        nxt = t2 - t1
        if nxt in said:
            _, t2 = said[nxt]
        else:
            t2 = t
        said[nxt] = (t2, t)
        last = nxt
        # Progress reporting
        if progress:
            if t % 1000000 == 0:
                print('.', end='', flush=True)
            elif t == turns - 1:
                print()
    return last


# %% Older code


# def ridx(data, x):
#     return len(data) - data[::-1].index(x) - 1


# # Test cases
# data = [0, 3, 6]
# # data = [1, 3, 2]
# # data = [2, 1, 3]
# # data = [1, 2, 3]
# # data = [2, 3, 1]
# # data = [3, 2, 1]
# # data = [3, 1, 2]

# # Old part 1
# n = len(data)
# turns = 2020
# for t in range(n, turns):
#     last = data[-1]
#     if data.count(last) == 1:
#         data.append(0)
#         continue
#     data.append(t - ridx(data[:-1], last) - 1)
# print(data[-1])
