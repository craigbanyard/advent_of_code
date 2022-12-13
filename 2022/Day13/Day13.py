from helper import aoc_timer
from dataclasses import dataclass
import math


def string_safe(s: str) -> bool:
    '''
    Solution uses `eval`, so ensure that the input file does not
    contain any malicious content that lead to unsafe `eval`.
    '''
    return not (s.islower() or s.isupper())


@aoc_timer
def get_input(path: str) -> list:
    with open(path) as f:
        lines = f.read()
        assert string_safe(lines), f'Potentially unsafe eval: {f}'
    return [eval(expr) for expr in lines.replace('\n\n', '\n').splitlines()]


def lt(a: int | list, b: int | list, result: bool | None = None) -> bool:
    '''Recursively compare a and b to determine whether a < b.'''
    if result is not None:
        return result
    match a, b:
        case int(), int():
            if a < b:
                result = True
            if a > b:
                result = False
        case list(), list():
            idx = 0
            while idx < len(b) and result is None:
                result = lt(a[idx], b[idx], result) if idx < len(a) else True
                idx += 1
            if idx < len(a) and result is None:
                result = False
        case int(), list():
            result = lt([a], b, result)
        case list(), int():
            result = lt(a, [b], result)
    return result


@dataclass
class Packet:
    value: list

    def __lt__(self, other: object) -> bool:
        try:
            return self.value < other.value
        except TypeError:
            return lt(self.value, other.value)


@aoc_timer
def solve(data: list) -> tuple[int, int]:
    P = [Packet(p) for p in data]
    DP = [Packet([[2]]), Packet([[6]])]
    ordered = sorted(P + DP)
    p1 = sum(idx * (p < q) for idx, (p, q) in
             enumerate(zip(P[::2], P[1::2]), start=1))
    p2 = math.prod((ordered.index(p) + 1) for p in DP)
    return p1, p2


# %% Output
def main() -> None:
    print("AoC 2022\nDay 13")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
