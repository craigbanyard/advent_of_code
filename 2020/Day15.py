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
