from helper import aoc_timer
from collections import defaultdict, deque
from copy import deepcopy
import re


@aoc_timer
def get_input(path: str) -> tuple[dict[int, deque], list[list[int]]]:
    crates, moves = open(path).read().split('\n\n')
    *crates, stacks = crates.splitlines()
    stack = defaultdict(deque)
    for crate in crates:
        for match in re.finditer(r'\w', crate):
            idx = int(stacks[match.start()])
            stack[idx].append(match.group())
    moves = [list(map(int, re.findall(r'\d+', move)))
             for move in moves.splitlines()]
    return stack, moves


@aoc_timer
def solve(stack: dict[int, deque], moves: list[list[int]], part1: bool) -> str:
    for n, source, dest in moves:
        move = deque()
        for _ in range(n):
            crate = stack[source].popleft()
            if part1:
                move.append(crate)
            else:
                move.appendleft(crate)
        for crate in move:
            stack[dest].appendleft(crate)
    return ''.join(v[0] for _, v in sorted(stack.items()))


# %% Output
def main() -> None:
    print("AoC 2022\nDay 05")
    S1, moves = get_input('input.txt')
    S2 = deepcopy(S1)
    print("Part 1:", solve(S1, moves, part1=True))
    print("Part 2:", solve(S2, moves, part1=False))


if __name__ == '__main__':
    main()
