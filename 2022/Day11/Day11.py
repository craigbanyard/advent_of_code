from helper import aoc_timer
from collections import deque
import math
import operator


class Monkey():

    OP = {
        '+': operator.add,
        '*': operator.mul
    }

    def __init__(self, notes: str) -> None:
        self.notes = notes
        self.items: deque[int] = None
        self.op: tuple(str, str, int | str) = None
        self.div: int = 0
        self.action: dict[bool, int] = {}
        self.activity: int = 0
        self.parse()

    def parse(self) -> None:
        for note in self.notes.splitlines()[1:]:
            match note.strip().split(': '):
                case 'Starting items', items:
                    self.items = deque(map(int, items.split(', ')))
                case 'Operation', equation:
                    *_, a, op, b = equation.split()
                    assert a == 'old', f'Invalid operation: {equation}'
                    b = int(b) if b.isdigit() else b
                    self.op = (a, op, b)
                case 'Test', test:
                    *_, d = test.split()
                    self.div = int(d)
                case 'If true', action:
                    *_, m = action.split()
                    self.action[True] = int(m)
                case 'If false', action:
                    *_, m = action.split()
                    self.action[False] = int(m)
                case _:
                    assert False, f'Invalid input line: {note}'

    def inspect(self, wrc: int, lcm: int) -> tuple[int, int]:
        self.activity += 1
        item = self.items.popleft()
        a, op, b = self.op
        b = item if a == b else b
        item = self.OP[op](item, b)
        # Integer division by the 'worry reduction coefficient'
        item //= wrc
        # Part 2 worry level management:
        # Reduce worry levels by the LCM of the divisors, which
        # equals their product since the divisors are coprime.
        item %= lcm
        mm = self.action[item % self.div == 0]
        return mm, item


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().split('\n\n')


def monkey_business(activity: list[int], n: int = 2) -> int:
    return math.prod(sorted(activity)[::-1][:n])


@aoc_timer
def solve(data: list[str], rounds: int, wrc: int) -> int:
    monkeys = [Monkey(notes) for notes in data]
    lcm = math.lcm(*[m.div for m in monkeys])
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
