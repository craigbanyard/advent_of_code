from helper import aoc_timer
from os import getcwd


@aoc_timer
def get_input(path):
    return [x.strip() for x in open(path).readlines()]


def all_idx(expr, val):
    return [idx for idx, x in enumerate(expr) if x == val]


def find_paren(expr, inner=True, reverse=False):
    S = []
    if reverse:
        L = len(expr) - 1
        for idx, ch in enumerate(expr[::-1]):
            if ch == ')':
                S.append(L - idx)
            elif ch == '(':
                left = (L - idx, S.pop())
                if inner:
                    return left
                if not S:
                    return left
        return S
    for idx, ch in enumerate(expr):
        if ch == '(':
            S.append(idx)
        elif ch == ')':
            left = (S.pop(), idx)
            if inner:
                return left
            if not S:
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
    lo, hi = find_paren(expr, inner=True)
    tmp = str(evaluate(expr[lo+1:hi]))
    nxt = ''.join(expr[:lo] + tmp + expr[hi+1:])
    return evaluate(nxt)


# Part 2
''' Order of operations has changed - now addition comes before multiplication
    All other rules remain the same
    Idea here is now to hack the input, placing parentheses either side of addition
    This will force the part 1 code to evaluate correctly for part 2 with no changes
'''


def add_paren(expr, idx):
    return expr[:idx-2] + '(' + expr[idx-2:idx+3] + ')' + expr[idx+3:]


def add_paren_behind(expr, idx, offset):
    offset += 2
    if expr[idx-2] == ')':
        lo, hi = find_paren(expr[:idx], inner=False, reverse=True)
        return expr[:lo] + '(' + expr[lo:idx+3] + ')' + expr[idx+3:], offset
    return add_paren(expr, idx), offset


def hack(expr):
    P = all_idx(expr, '+')
    offset = 0
    for i, idx in enumerate(P):
        idx += offset
        while expr[idx] != '+':
            idx += 1
        assert expr[idx] == '+'
        # End of expression => add parentheses and return
        if len(expr) - idx <= 3:
            return add_paren_behind(expr, idx, offset)[0]
        # Open behind => skip
        if expr[idx-3] == '(':
            continue
        # Close ahead
        if expr[idx+3] == ')':
            expr, offset = add_paren_behind(expr, idx, offset)
            continue
        # Open ahead, close behind => encase the whole lot
        if expr[idx+2] == '(':
            _, hi = [(idx + 2) + x for x in find_paren(expr[idx+2:], inner=False, reverse=False)]
            # Close behind
            if expr[idx-2] == ')':
                lo, _ = find_paren(expr[:idx], inner=False, reverse=True)
                new = expr[:lo] + '(' + expr[lo:hi] + ')' + expr[hi:]
                if i < len(P) - 1:
                    if hi > P[i+1]:
                        offset += 1
                        expr = new
                        continue
                offset += 2
                expr = new
                continue
            new = expr[:idx-2] + '(' + expr[idx-2:hi] + ')' + expr[hi:]
            if i < len(P) - 1:
                if hi > P[i+1]:
                    offset += 1
                    expr = new
                    continue
            offset += 2
            expr = new
            continue
        # Nothing special
        expr, offset = add_paren_behind(expr, idx, offset)
    return expr


@aoc_timer
def Day18(data, part1=True):
    ans = 0
    for expr in data:
        if part1:
            ans += evaluate(expr)
        else:
            expr = hack(expr)
            ans += evaluate(expr)
    return ans


# %% Output
def main():
    path = getcwd() + "\\Inputs\\Day18.txt"
    # path = getcwd() + "\\Inputs\\Samples\\Day18.txt"
    print("AoC 2020\nDay 18")
    data = get_input(path)
    print("Part 1:", Day18(data, True))
    print("Part 2:", Day18(data, False))


if __name__ == '__main__':
    main()


'''
%timeit get_input(path)
268 µs ± 206 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit Day18(data, True)
54.3 ms ± 61.3 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit Day18(data, False)
73.2 ms ± 94.5 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
'''

# DEBUG:
# path = getcwd() + "\\Inputs\\Samples\\Day18.txt"
# data = get_input(path)

# for expr in data:
#     print(expr, '=', end=' ')
#     print(evaluate(expr))
#     expr = hack(expr)
#     print(expr, '=', end=' ')
#     print(evaluate(expr))
