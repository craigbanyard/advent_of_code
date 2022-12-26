from helper import aoc_timer
from collections import deque
from dataclasses import dataclass
import itertools as it


@dataclass
class SNAFU:
    n: str

    # Mapping table (a + b) = (digit, carry)
    ADD = {
        ('=', '='): ('1', '-'),
        ('=', '-'): ('2', '-'),
        ('=', '0'): ('=', '0'),
        ('=', '1'): ('-', '0'),
        ('=', '2'): ('0', '0'),
        ('-', '='): ('2', '-'),
        ('-', '-'): ('=', '0'),
        ('-', '0'): ('-', '0'),
        ('-', '1'): ('0', '0'),
        ('-', '2'): ('1', '0'),
        ('0', '='): ('=', '0'),
        ('0', '-'): ('-', '0'),
        ('0', '0'): ('0', '0'),
        ('0', '1'): ('1', '0'),
        ('0', '2'): ('2', '0'),
        ('1', '='): ('-', '0'),
        ('1', '-'): ('0', '0'),
        ('1', '0'): ('1', '0'),
        ('1', '1'): ('2', '0'),
        ('1', '2'): ('=', '1'),
        ('2', '='): ('0', '0'),
        ('2', '-'): ('1', '0'),
        ('2', '0'): ('2', '0'),
        ('2', '1'): ('=', '1'),
        ('2', '2'): ('-', '1')
    }
    A = {
        '2': '2',
        '1': '1',
        '0': '0',
        '-': '0',
        '=': '0'
    }
    B = {
        '2': '0',
        '1': '0',
        '0': '0',
        '-': '1',
        '=': '2'
    }

    def __add__(self, other: type['SNAFU']) -> type['SNAFU']:
        result = deque([])
        carry = '0'
        a, b = reversed(self.n), reversed(other.n)
        for p, q in it.zip_longest(a, b, fillvalue='0'):
            d, c = self.ADD[(p, q)]
            dd, cc = self.ADD[(d, carry)]
            carry, _ = self.ADD[(c, cc)]
            assert _ == '0'
            result.appendleft(dd)
        if carry != '0':
            result.appendleft(carry)
        return SNAFU(''.join(result))

    def __repr__(self) -> str:
        return self.n

    def dec(self) -> int:
        a, b = '', ''
        for d in self.n:
            a += self.A[d]
            b += self.B[d]
        return int(a, 5) - int(b, 5)


@aoc_timer
def get_input(path: str) -> list[str]:
    return open(path).read().splitlines()


@aoc_timer
def solve(data: list[str]) -> str:
    return sum([SNAFU(n) for n in data], start=SNAFU('0'))


# %% Output
def main() -> None:
    print("AoC 2022\nDay 25")
    data = get_input('input.txt')
    print("Part 1:", solve(data))


if __name__ == '__main__':
    main()
