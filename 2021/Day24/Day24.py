from helper import aoc_timer
from collections import deque


@aoc_timer
def get_input(path):
    return [line.split() for line in open(path).read().splitlines()]


def alu_naive(data, model_number):
    '''Perform the full ALU instruction set on an input model number.'''
    assert len(model_number) == 14, f'Invalid model number: {model_number}'
    model_number = deque([*map(int, model_number)])
    vars = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }
    for instr in data:
        b = instr[-1]
        b = vars[b] if b in vars else int(b)
        match instr:
            case ['inp', a]:
                vars[a] = model_number.popleft()
            case ['add', a, _]:
                vars[a] += b
            case ['mul', a, _]:
                vars[a] *= b
            case ['div', a, _]:
                vars[a] //= b
            case ['mod', a, _]:
                vars[a] %= b
            case ['eql', a, _]:
                vars[a] = 1 if vars[a] == b else 0
            case _:
                assert False, instr
    return vars['z']


def get_alu_vars(data):
    '''Return a generator for the three ALU variables, a, b, c.'''
    for idx in range(0, len(data), 18):
        a = int(data[idx + 4][-1])
        b = int(data[idx + 5][-1])
        c = int(data[idx + 15][-1])
        yield (a, b, c)


def alu(data, model_number):
    '''Perform the reduced ALU instruction set on an input model number.'''
    assert len(model_number) == 14, f'Invalid model number: {model_number}'
    model_number = deque([*map(int, model_number)])
    w = x = z = 0
    for (a, b, c) in get_alu_vars(data):
        w = model_number.popleft()
        x = (z % 26) + b != w
        z // a
        z *= (25 * x + 1)
        x += x * (w + c)
    return z


@aoc_timer
def Day24(data):
    '''
    Assumptions following deconstruction of my input in Excel:

    The input instructions are the same 18 operations repeated 14 times, once
    for each digit of the model number, with 3 possible variations each time:

        |-----|------------|-----|
        | idx | instr.     | eq  |
        |-----|------------|-----|
        | 0   | inp w      | (0) |
        | 1   | mul x 0    | (1) |
        | 2   | add x z    | (1) |
        | 3   | mod x 26   | (1) |
        | 4   | div z {a}  | (2) |  <- variable 1
        | 5   | add x {b}  | (1) |  <- variable 2
        | 6   | eql x w    | (1) |
        | 7   | eql x 0    | (1) |
        | 8   | mul y 0    | (3) |
        | 9   | add y 25   | (3) |
        | 10  | mul y x    | (3) |
        | 11  | add y 1    | (3) |
        | 12  | mul z y    | (3) |
        | 13  | mul y 0    | (4) |
        | 14  | add y w    | (4) |
        | 15  | add y {c}  | (4) |  <- variable 3
        | 16  | mul y x    | (4) |
        | 17  | add z y    | (4) |
        |-----|------------|-----|

    Each set of instructions can then be distilled down to:
    w = input()             (0)
    x = (z % 26) + b != w   (1)
    z // a                  (2)
    z *= (25 * x + 1)       (3)
    z += x * (w + c)        (4)

    Furthermore, a ∈ {1, 26}. Where a == 1, we have:
    (0) w = input()     remains unchanged
    (1) x = 1           11 <= b <= 15 in these cases ⇒ w < (z % 26) + b
    (2) z               z // 1 == z ∀ z
    (3) z *= 26         x == 1 from (1) above
    (4) z += (w + c)    x == 1 from (1) above

    Where a == 26, we require that (z % 26) + b == w
    ⇔ w' + c' == w - b
    where w' and c' are w and c from the previous a == 1 instruction
    We can think of z as a stack, where a == 1 pushes and a == 26 pops.
    '''

    relativities = {}
    stack = deque()
    for i, (a, b, c) in enumerate(get_alu_vars(data)):
        if a == 26:
            j, c = stack.pop()
            relativities[i] = (j, c + b)
        else:
            stack.append((i, c))

    # Initial guess for each digit (g):
        # Part 1: 9 ⇒ require min(9, 9 ± 𐤃) ⇔ maximum for MONAD
        # Part 2: 1 ⇒ require max(1, 1 ± 𐤃) ⇔ minimum for MONAD
    for f, g in [(min, 9), (max, 1)]:
        model_number = {}
        for i, (j, delta) in relativities.items():
            model_number[i] = f(g, g + delta)
            model_number[j] = f(g, g - delta)
        yield ''.join(str(model_number[idx]) for idx in range(14))


# %% Output
def main():
    print("AoC 2021\nDay 24")
    data = get_input('input.txt')
    p1, p2 = Day24(data)
    assert (z := alu(data, p1)) == 0, f'{p1} -> {z}'
    assert (z := alu(data, p2)) == 0, f'{p2} -> {z}'
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
