from helper import aoc_timer


@aoc_timer
def get_input(path):
    return [line.split() for line in open(path).read().splitlines()]


@aoc_timer
def solve(data, part):
    W = 6
    D = 3
    score = {
        'A': 1,
        'B': 2,
        'C': 3
    }
    win = {
        'A': 'B',
        'B': 'C',
        'C': 'A'
    }
    lose = {
        'A': 'C',
        'B': 'A',
        'C': 'B'
    }
    strategy = {
        1: {
            'X': lambda x: 'A',
            'Y': lambda x: 'B',
            'Z': lambda x: 'C'
        },
        2: {
            'X': lambda x: lose[x],
            'Y': lambda x: x,
            'Z': lambda x: win[x]
        }
    }
    total = 0
    for p, q in data:
        play = strategy[part][q](p)
        if p == play:
            total += + D
        elif play == win[p]:
            total += + W
        total += score[play]
    return total


# %% Output
def main():
    print("AoC 2022\nDay 02")
    data = get_input('input.txt')
    print("Part 1:", solve(data, part=1))
    print("Part 2:", solve(data, part=2))


if __name__ == '__main__':
    main()
