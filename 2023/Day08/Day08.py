# %% Day 08
from helper import aoc_timer
import itertools as it
from math import lcm


@aoc_timer
def get_input(path: str) -> tuple[str, dict[str, tuple[str]]]:
    instr, network = open(path).read().split('\n\n')
    N = {}
    for node in network.splitlines():
        a, b = node.rstrip(')').split(' = (')
        N[a] = tuple(b.split(', '))
    return instr, N


@aoc_timer
def solve(data: tuple[str, dict[str, tuple[str]]],
          start_suffix: str = 'AAA', end_suffix: str = 'ZZZ') -> int:
    D = {
        'L': 0,
        'R': 1
    }
    instr, network = data
    nodes = [k for k in network if k.endswith(start_suffix)]
    cycles = []
    for step, d in enumerate(it.cycle(instr), start=1):
        new = []
        for node in nodes:
            if (nxt := network[node][D[d]]).endswith(end_suffix):
                cycles.append(step)
                continue
            new.append(nxt)
        if not new:
            return lcm(*cycles)
        nodes = new


def main() -> None:
    print("AoC 2023\nDay 08")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, start_suffix='A', end_suffix='Z'))


if __name__ == '__main__':
    main()
