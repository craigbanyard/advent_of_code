from helper import aoc_timer
from hashlib import md5


@aoc_timer
def get_input(path):
    return open(path).read()


def check_hash(s, N, chars):
    h = md5(s.encode()).hexdigest()
    if h[0:N] == '0' * N:
        pos = int(h[N], 16)
        if pos in range(chars):
            return h[N], (pos, h[N + 1])
        return h[N], None
    return None


def print_progress(prog_bar, p1, p2, prog):
    if not prog:
        return None
    prog_p1 = f"Part 1: {''.join(p1)} | "
    prog_p2 = f"Part 2: {''.join(p2)} | "
    prog_bar += '█'
    print('\r', end='')
    print(f"{prog_p1}{prog_p2}{prog_bar}", end='', flush=True)
    return prog_bar


@aoc_timer
def Day05(key, N, chars, prog=False):
    n = 1
    idx1 = 0
    found = 0
    disp_flag = False
    p1 = ['_' for _ in range(chars)]
    p2 = p1.copy()
    prog_bar = 'Hacking... '
    prog_bar = print_progress(prog_bar, p1, p2, prog)
    while found < chars:
        s = key + str(n)
        if h := check_hash(s, N, chars):
            h1, h2 = h
            if idx1 < chars:
                p1[idx1] = h1
                idx1 += 1
                disp_flag = True
            if h2:
                idx2, h2 = h2
                if p2[idx2] == '_':
                    p2[idx2] = h2
                    found += 1
                    disp_flag = True
        n += 1
        if prog and (disp_flag or n % 1e6 == 0):
            prog_bar = print_progress(prog_bar, p1, p2, prog)
            disp_flag = False
    prog_bar = print_progress(prog_bar, p1, p2, prog)
    if prog:
        print('\nHack complete!')
    return ''.join(p1), ''.join(p2)


# %% Output
def main():
    print("AoC 2016\nDay 05")
    key = get_input('input.txt')
    p1, p2 = Day05(key, N=5, chars=8, prog=True)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
