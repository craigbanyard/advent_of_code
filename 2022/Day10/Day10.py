from helper import aoc_timer
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[str]:
    yield from open(path).read().splitlines()


@aoc_timer
def solve(data: Iterator[str], **kwargs: str) -> tuple[int, str]:
    global p1, p2

    x = 1
    cycle = 1
    p1, p2 = 0, '\n'
    W = 40
    ON, OFF = kwargs.get('on', '#'), kwargs.get('off', '.')

    def process():
        '''Perform clock cycle operation.'''
        global p1, p2
        if cycle % W == 20:
            p1 += x * cycle
        if x - 1 <= (cycle - 1) % W <= x + 1:
            p2 += ON
        else:
            p2 += OFF
        if cycle % W == 0:
            p2 += '\n'

    for instr in data:
        process()
        if instr != 'noop':
            _, n = instr.split()
            cycle += 1
            process()
            x += int(n)
        cycle += 1
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 10")
    data = get_input('input.txt')
    p1, p2 = solve(data, on='█', off=' ')
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
