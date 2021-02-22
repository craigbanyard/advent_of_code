from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [int(x) for x in open(path).read().split(',')]


@aoc_timer
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
        if progress and t % 1000000 == 0:
            print('.', end='', flush=True)
    if progress:
        print()
    return last


# %% Output
def main():
    print("AoC 2020\nDay 15")
    data = get_input('input.txt')
    print("Part 1:", Day15(data))
    print("Part 2:", Day15(data, turns=30000000, progress=True))


if __name__ == '__main__':
    main()
