from helper import aoc_timer
from ast import literal_eval
import itertools as it
import re


@aoc_timer
def get_input(path):
    return [*open(path).read().splitlines()]


def add(a, b):
    return f'[{a},{b}]'


def explode(expr):
    stack = []
    i = j = None
    for idx, ch in enumerate(expr):
        if ch == '[':
            stack.append(idx)
        elif ch == ']':
            i = stack.pop()
            if len(stack) == 4:
                j = idx + 1
                break
    if j is None:
        return expr, False
    a, b = literal_eval(expr[i:j])
    nums, ends = {}, {}
    L = R = None
    for match in re.finditer(r'\d+', expr):
        start_idx = match.start()
        nums[start_idx] = int(match.group())
        ends[start_idx] = match.end()
        if start_idx < i:
            L = start_idx
        if start_idx > j and R is None:
            R = start_idx
    left = expr[:i]
    right = expr[j:]
    if L:
        a += nums[L]
        left = f'{expr[:L]}{a}{expr[ends[L]:i]}'
    if R:
        b += nums[R]
        right = f'{expr[j:R]}{b}{expr[ends[R]:]}'
    return f'{left}0{right}', True


def split(expr):
    for match in re.finditer(r'\d+', expr):
        n = int(match.group())
        if n > 9:
            i, j = match.start(), match.end()
            m = n // 2
            n -= m
            return f'{expr[:i]}[{m},{n}]{expr[j:]}', True
    return expr, False


def reduce(expr):
    diff = True
    while diff:
        expr, diff = explode(expr)
    expr, diff = split(expr)
    if diff:
        return reduce(expr)
    return expr


def magnitude(expr: list) -> int:
    match expr:
        case str():
            return magnitude(literal_eval(expr))
        case list():
            a, b = expr
            return 3 * magnitude(a) + 2 * magnitude(b)
        case _:
            return expr


@aoc_timer
def Day18(data):
    ans, *b = data
    for expr in b:
        ans = reduce(add(ans, expr))
    p2 = 0
    for a, b in it.permutations(data, 2):
        p2 = max(p2, magnitude(reduce(add(a, b))))
    return magnitude(ans), p2


class UnitTest:

    EXP = {
        '[[[[[9,8],1],2],3],4]': '[[[[0,9],2],3],4]',
        '[7,[6,[5,[4,[3,2]]]]]': '[7,[6,[5,[7,0]]]]',
        '[[6,[5,[4,[3,2]]]],1]': '[[6,[5,[7,0]]],3]',
        '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]': '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
        '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]': '[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
        '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]': '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]',
        '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]': '[[[[0,7],4],[15,[0,13]]],[1,1]]',
        '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',
        '[[[[0,7],4],[15,[0,13]]],[1,1]]': '[[[[0,7],4],[15,[0,13]]],[1,1]]',
        '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]': '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
    }

    SPL = {
        '[[[[0,7],4],[15,[0,13]]],[1,1]]': '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]',
        '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]': '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
    }

    RED = {
        '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',
        '[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]]': '[[[[3,0],[5,3]],[4,4]],[5,5]]',
        '[[[[[3,0],[5,3]],[4,4]],[5,5]],[6,6]]': '[[[[5,0],[7,4]],[5,5]],[6,6]]'
    }

    MAG = {
        '[9,1]': 29,
        '[[9,1],[1,9]]': 129,
        '[[1,2],[[3,4],5]]': 143,
        '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]': 1384,
        '[[[[1,1],[2,2]],[3,3]],[4,4]]': 445,
        '[[[[3,0],[5,3]],[4,4]],[5,5]]': 791,
        '[[[[5,0],[7,4]],[5,5]],[6,6]]': 1137,
        '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]': 3488
    }

    def __init__(self):
        self.tests = {
            'EXP': (explode, self.EXP),
            'SPL': (split, self.SPL),
            'RED': (reduce, self.RED),
            'MAG': (magnitude, self.MAG)
        }

    def run(self):
        for name, (f, dict) in self.tests.items():
            for k, v in dict.items():
                match (a := f(k)):
                    case tuple():
                        actual, _ = a
                    case _:
                        actual = a
                result = 'Pass' if actual == v else f'Fail, expected: {v}'
                print(f'{name}: {k} -> {actual} ({result})')


# %% Output
def main():
    print("AoC 2021\nDay 18")
    data = get_input('input.txt')
    p1, p2 = Day18(data)
    print("Part 1:", p1)
    print("Part 2:", p2)
    # UnitTest().run()


if __name__ == '__main__':
    main()
