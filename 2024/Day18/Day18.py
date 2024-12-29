# %% Day 18
from helper import aoc_timer, Colours, Grid
from io import StringIO
from typing import Iterator

type Data = Iterator[tuple[int, int]]
type Node = tuple[int, int]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        yield from [tuple(map(int, line.split(","))) for line in f.read().splitlines()]


def visualise(memory: Grid, path: set[Node], block: Node | None = None) -> None:
    out = StringIO()
    path_marker = Colours.highlight("O", [Colours.BOLD, Colours.fg.CYAN])
    block_marker = Colours.highlight("#", Colours.fg.LIGHTRED)
    for r in range(memory._R):
        for c in range(memory._C):
            if (r, c) == block:
                out.write(block_marker)
            elif (r, c) in path:
                out.write(path_marker)
            else:
                out.write(memory.G[r][c])
        out.write("\n")
    print(out.getvalue())


@aoc_timer
def solve(data: Data, s: int = 70, t: int = 1024, vis: bool = False) -> tuple[int, str]:
    memory = Grid(G=[["." for _ in range(s + 1)] for _ in range(s + 1)])
    start, end = (0, 0), (s, s)
    for _ in range(t):
        c, r = next(data)
        memory.G[r][c] = "#"
    optimal = memory.optimal_path(start, end, "bfs")
    p1 = len(optimal) - 1
    if vis:
        visualise(memory, optimal)
    while True:
        c, r = next(data)
        memory.G[r][c] = '#'
        if (r, c) not in optimal:
            continue
        if vis:
            prev = optimal.copy()
        optimal = memory.optimal_path(start, end, "bfs")
        if not optimal:
            p2 = f"{c},{r}"
            if vis:
                visualise(memory, prev, (r, c))
            break
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 18")
    data = get_input("input.txt")
    p1, p2 = solve(data, vis=True)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
