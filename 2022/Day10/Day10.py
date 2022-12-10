from helper import aoc_timer
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[str]:
    yield from open(path).read().splitlines()


@aoc_timer
def solve(data: Iterator[str]) -> tuple[int, str]:
    global p1, p2

    x = 1
    cycle = 1
    periods = range(20, 221, 40)
    p1, p2 = 0, '\n'
    Q = []
    W = 40
    ON, OFF = '#', ' '

    def process():
        '''Perform clock cycle operation.'''
        global p1, p2
        if cycle in periods:
            p1 += x * cycle
        if x - 1 <= (cycle - 1) % W <= x + 1:
            p2 += ON
        else:
            p2 += OFF
        if cycle % W == 0:
            p2 += '\n'

    for op in data:
        process()
        if op != 'noop':
            _, n = op.split()
            Q.append(int(n))
        while Q:
            cycle += 1
            process()
            x += Q.pop()
        cycle += 1
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 10")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
