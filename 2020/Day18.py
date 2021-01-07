from helper import aoc_timer
from os import getcwd
import math


@aoc_timer
def get_input(path, func, time=True):
    for expr in open(path).read().split('\n'):
        yield func(expr)


def find_paren(expr):
    S = []
    for idx, ch in enumerate(expr):
        if ch == '(':
            S.append(idx)
        elif ch == ')':
            left = (S.pop(), idx)
            if not S:
                return left
            return left
    return S


def evaluate(expr):
    # No parentheses
    if not any(x in expr for x in '()'):
        # Edge case - already reduced to a single number
        if expr.count(' ') == 0:
            return int(expr)
        a, op, b, *rest = expr.split()
        tmp = eval(''.join(a + op + b))
        if rest:
            nxt = str(tmp) + ' ' + ' '.join(rest)
            return evaluate(nxt)
        return tmp
    # Parentheses
    lo, hi = find_paren(expr)
    tmp = str(evaluate(expr[lo+1:hi]))
    nxt = ''.join(expr[:lo] + tmp + expr[hi+1:])
    return evaluate(nxt)


def evaluate_p2(expr):
    if any(x in expr for x in '()'):
        lo, hi = find_paren(expr)
        tmp = str(math.prod(evaluate(e) for e in expr[lo+1:hi].split(' * ')))
        nxt = ''.join(expr[:lo] + tmp + expr[hi+1:])
        return evaluate_p2(nxt)
    return math.prod(evaluate(e) for e in expr.split(' * '))


@aoc_timer
def Day18(path, part1=True):
    if part1:
        return sum(get_input(path, evaluate))
    return sum(get_input(path, evaluate_p2, time=False))


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day18.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day18.txt"
    print("AoC 2020\nDay 18")
    print("Part 1:", Day18(path, True))
    print("Part 2:", Day18(path, False))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
268 µs ± 206 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day18(data, True)
54.3 ms ± 61.3 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit Day18(path, False)
38.9 ms ± 117 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
'''
