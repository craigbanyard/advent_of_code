from helper import aoc_timer
from collections import deque
from copy import deepcopy
import math
import operator
import re
from typing import Callable


class Monkey():
    OP = {
        '+': operator.add,
        '*': operator.mul
    }

    def __init__(self, notes: list[str]) -> None:
        self.notes = notes
        self.items: deque[int] = None
        self.op: Callable[[int], int] = None
        self.div: int = None
        self.action: dict[bool, int] = {}
        self.activity: int = 0
        self.parse()

    def __eq__(self, __o: object) -> bool:
        '''Implemented for unit testing.'''
        return self.notes == __o.notes

    def parse(self) -> None:
        _, items, operation, *test = self.notes
        num_pattern = re.compile(r'\d+')
        self.items = deque(map(int, num_pattern.findall(items)))
        *_, op, b = operation.split()
        self.op = lambda a: self.OP[op](a, int(b) if b.isdigit() else a)
        parse_test = map(int, num_pattern.findall(''.join(test)))
        self.div, self.action[True], self.action[False] = parse_test

    def inspect(self, wrc: int, lcm: int) -> tuple[int, int]:
        self.activity += 1
        item = self.items.popleft()
        item = self.op(item)
        # Integer division by the 'worry reduction coefficient'
        item //= wrc
        # Part 2 worry level management:
        # Reduce worry levels by the LCM of the divisors, which
        # equals their product since the divisors are coprime
        item %= lcm
        mm = self.action[item % self.div == 0]
        return mm, item


@aoc_timer
def get_input(path: str) -> list[Monkey]:
    return [Monkey(notes.split('\n'))
            for notes in open(path).read().split('\n\n')]


def monkey_business(activity: list[int], n: int = 2) -> int:
    return math.prod(sorted(activity)[-n:])


@aoc_timer
def solve(data: list[Monkey], rounds: int, wrc: int) -> int:
    # Monkey is a mutable object so requires a deepcopy for use
    # in both parts
    monkeys = deepcopy(data)
    lcm = math.prod([m.div for m in monkeys])
    for _ in range(rounds):
        for m in monkeys:
            while m.items:
                mm, item = m.inspect(wrc, lcm)
                monkeys[mm].items.append(item)
    return monkey_business([m.activity for m in monkeys])


# %% Output
def main() -> None:
    print("AoC 2022\nDay 11")
    data = get_input('input.txt')
    print("Part 1:", solve(data, rounds=20, wrc=3))
    print("Part 2:", solve(data, rounds=10000, wrc=1))


if __name__ == '__main__':
    main()
