# %% Day 15
from helper import aoc_timer, Colours
from collections import defaultdict, deque
import numpy as np

type Data = tuple[np.ndarray, str]

W, S, B, BL, BR, R = 0, 1, 2, 3, 4, 5
UPSCALE = {"#": "##", ".": "..", "O": "[]", "@": "@."}
MAP = {"#": W, ".": S, "O": B, "[": BL, "]": BR, "@": R}


@aoc_timer
def get_input(path: str, upscaled: bool = False) -> Data:
    with open(path) as f:
        w, m = f.read().split("\n\n")
        if upscaled:
            for k, v in UPSCALE.items():
                w = w.replace(k, v)
        w = np.array(
            [list(map(MAP.get, [*line])) for line in w.splitlines()], dtype=np.byte
        )
    return w, m.replace("\n", "")


def view(warehouse: np.ndarray, prefix: str = "") -> None:
    w = warehouse.astype("object")
    for k, v in MAP.items():
        if k == "@":
            k = f"{Colours.fg.CYAN}{k}{Colours.ENDC}"
        w[w == v] = k
    print(f"{prefix}{"\n".join("".join(c for c in r) for r in w)}")


def robot(warehouse: np.ndarray) -> tuple[int, int]:
    r, c = np.where(warehouse == R)
    return r[0], c[0]


def scan(a: np.ndarray, e: int, d: int) -> int | None:
    (idx,) = np.where(a[::d] == e)
    if len(idx):
        return idx[0] + 1
    return None


def move(a: np.ndarray, r: int, c: int, d: int) -> tuple[np.ndarray, int]:
    visited = set()
    columns = defaultdict(list)
    Q = deque([(r, c)])
    while Q:
        r, c = Q.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        columns[c].append(r)
        if a[(r, c)] == S:
            continue
        rr = r + d
        if a[(rr, c)] == W:
            return a, 0
        elif a[(rr, c)] == BL:
            Q.append((rr, c + 1))
        elif a[(rr, c)] == BR:
            Q.append((rr, c - 1))
        Q.append((rr, c))
    for c, r in columns.items():
        a[r, c] = np.roll(a[r, c], 1)
    return a, d


def gps(warehouse: np.ndarray, box: int) -> int:
    r, c = np.where(warehouse == box)
    return (100 * r + c).sum()


@aoc_timer
def solve(data: Data, upscaled: bool = False, vis: bool = False) -> int:
    warehouse, moves = data
    M = {
        "<": lambda r, c: ((r, slice(0, c + 1)), 0, -1),
        ">": lambda r, c: ((r, slice(c, None)), 0, 1),
        "^": lambda r, c: ((slice(0, r + 1), c), -1, 0),
        "v": lambda r, c: ((slice(r, None), c), 1, 0),
    }
    if vis:
        view(warehouse, prefix="Initial state:\n")
    r, c = robot(warehouse)
    for m in moves:
        slc, dr, dc = M[m](r, c)
        d = dr or dc
        if upscaled and m in "^v":
            warehouse, dr = move(warehouse, r, c, d)
        elif (s := scan(warehouse[slc], S, d)) is None:
            continue
        elif s > scan(warehouse[slc], W, d):
            continue
        if not upscaled or m in "<>":
            warehouse[slc][::d][:s] = np.roll(warehouse[slc][::d][:s], 1)
        r += dr
        c += dc
    if vis:
        view(warehouse, prefix="\nFinal state:\n")
    return gps(warehouse, BL if upscaled else B)


def main() -> None:
    print("AoC 2024\nDay 15")
    data = get_input("input.txt")
    print("Part 1:", solve(data))
    data = get_input("input.txt", upscaled=True)
    print("Part 2:", solve(data, upscaled=True))


if __name__ == "__main__":
    main()
