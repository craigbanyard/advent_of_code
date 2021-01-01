from helper import aoc_timer


def hash_cups(data, mod=9):
    data = str(data)
    mx, last = len(data), int(data[-1])
    cups = {int(a): int(b) for a, b in zip(data, data[1:])}
    while mod > mx:
        cups[last] = mx + 1
        last = (mx := mx + 1)
    cups[last] = int(data[0])
    return cups


def mod_inc(n, i=1, m=9):
    ans = (n + i) % m
    if not ans:
        ans = m
    return ans


def turn(cup, cups, mod=9):
    pick = []
    dest = mod_inc(cup, -1, mod)
    for _ in range(3):
        # cup = cups[cup]
        pick.append(cup := cups[cup])
        while dest in pick:
            dest = mod_inc(dest, -1, mod)
    return tuple(pick), cups[cup], dest, cups[dest]


def p1_ans(cups, cup=1, mod=9):
    ans = ''
    for _ in range(mod - 1):
        cup = cups[cup]
        ans += str(cup)
    return ans


def p2_ans(cups, cup=1, n=2):
    ans = 1
    for _ in range(n):
        ans *= (cup := cups[cup])
    return ans


@aoc_timer
def play(data, mod=9, moves=100, part1= True, output=False):
    cups = hash_cups(data, mod)
    cup = int(str(data)[0])
    for m in range(moves):
        pick, ncup, a, b = turn(cup, cups, mod)
        if output:
            print(f"-- move {m+1} --\n({cup}), {cups}\npick up: {pick}\n" +
                  f"next cup: ({ncup})\ndestination: {a}\n")
        cups[cup] = ncup
        cups[a] = pick[0]
        cups[pick[-1]] = b
        cup = ncup
    if output:
        print(f"-- final --\ncups: ({cup}) {cups}")
    if part1:
        return p1_ans(cups)
    return p2_ans(cups)


# %% Output
def main():
    data = 589174263
    print("AoC 2020\nDay 23")
    print("Part 1:", play(data))
    print("Part 2:", play(data, 1000000, 10000000, False, False))


if __name__ == '__main__':
    main()
