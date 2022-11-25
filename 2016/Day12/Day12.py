from helper import aoc_timer


def to_int(x):
    try:
        return int(x)
    except ValueError:
        return x


@aoc_timer
def get_input(path: str) -> list[str | int]:
    return [list(map(to_int, line.split()))
            for line in open(path).readlines()]


@aoc_timer
def Day12(data: list[str], init=0) -> int:
    registers = {
        'a': 0,
        'b': 0,
        'c': init,
        'd': 0
    }
    instructions = {
        'inc': 1,
        'dec': -1
    }
    max_idx = len(data) - 1
    idx = 0

    while True:
        match data[idx]:
            case [action, x]:
                registers[x] += instructions[action]
            case [action, x, y]:
                value = registers[x] if x in registers else x
                if y in registers:
                    registers[y] = value
                elif value != 0:
                    idx += y - 1
        idx += 1
        if idx > max_idx:
            break

    return registers['a']


def main():
    print("AoC 2016\nDay 12")
    data = get_input('input.txt')
    print("Part 1:", Day12(data))
    print("Part 2:", Day12(data, init=1))


if __name__ == '__main__':
    main()
