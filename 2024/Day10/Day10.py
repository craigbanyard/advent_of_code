# %% Day 10
from helper import aoc_timer, Grid
from collections import deque
from typing import Iterator

type Data = list[list[int]]
type Node = tuple[int, int]


def parse_int(n: str, default: int = -1) -> int:
    """For sample inputs containing '.' characters."""
    try:
        return int(n)
    except ValueError:
        return default


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        return [[*map(parse_int, line)] for line in f.read().splitlines()]


class Map(Grid):

    def neighbours(self, r: int, c: int) -> Iterator[Node]:
        for dr, dc in self.D:
            if 0 <= (rr := r + dr) < self._R and 0 <= (cc := c + dc) < self._C:
                if self.G[rr][cc] - self.G[r][c] == 1:
                    yield (rr, cc)

    def bfs(self, start: int, end: int) -> dict[Node, list[Node]]:
        start_nodes = [*self.where(start)]
        trailheads = {node: [] for node in start_nodes}
        Q = deque(zip(start_nodes, start_nodes))
        while Q:
            head, (r, c) = Q.popleft()
            if self.G[r][c] == end:
                trailheads[head].append((r, c))
                continue
            for new_pos in self.neighbours(r, c):
                Q.append((head, new_pos))
        return trailheads


@aoc_timer
def solve(data: Data) -> tuple[int, int]:
    m = Map(G=data)
    p1 = p2 = 0
    for v in m.bfs(0, 9).values():
        p1 += len(set(v))
        p2 += len(v)
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 10")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
