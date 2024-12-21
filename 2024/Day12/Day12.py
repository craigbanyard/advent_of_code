# %% Day 12
from helper import aoc_timer, Colours, Grid
from collections import deque
from io import StringIO
from string import ascii_uppercase
from typing import Iterator

type Data = list[str]
type Node = tuple[int, int]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        return f.read().splitlines()


def view(data: Data) -> None:
    colours = [
        Colours.fg.RED,
        Colours.fg.GREEN,
        Colours.fg.BLUE,
        Colours.fg.YELLOW,
        Colours.fg.PURPLE,
        Colours.fg.CYAN,
        Colours.fg.LIGHTRED,
        Colours.fg.LIGHTGREEN,
        Colours.fg.LIGHTBLUE,
        Colours.fg.PINK,
        Colours.fg.LIGHTCYAN,
    ]
    n = len(colours)
    char_colours = {ch: colours[idx % n] for idx, ch in enumerate(ascii_uppercase)}
    out = StringIO()
    for r in data:
        for c in r:
            out.write(Colours.highlight(c, char_colours[c]))
        out.write("\n")
    print(f"\n{out.getvalue()}")


class Map(Grid):

    D = [
        (0, 1),     # Right
        (1, 0),     # Down
        (0, -1),    # Left
        (-1, 0),    # Up
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.visited = set()
        self.regions = {}
        self.exterior = {}
        self.a = {}
        self.p = {}
        self.s = {}

    def neighbours(self, r: int, c: int) -> Iterator[Node]:
        for dr, dc in self.D:
            if 0 <= (rr := r + dr) < self._R and 0 <= (cc := c + dc) < self._C:
                if self.G[rr][cc] == self.G[r][c]:
                    yield (rr, cc)

    def boundary(self, r: int, c: int) -> bool:
        for dr, dc in self.D + self.DD:
            if not (0 <= (rr := r + dr) < self._R and 0 <= (cc := c + dc) < self._C):
                return True
            if self.G[rr][cc] != self.G[r][c]:
                return True
        return False

    def bfs(self, start: Node) -> set[Node]:
        v0 = len(self.visited)
        self.visited.add(start)
        bounds = set()
        self.p[start] = 0
        Q = deque([start])
        while Q:
            pos = Q.popleft()
            if self.boundary(*pos):
                bounds.add(pos)
            self.regions[pos] = start
            self.p[start] += 4
            for new_pos in self.neighbours(*pos):
                self.p[start] -= 1
                if new_pos in self.visited:
                    continue
                self.visited.add(new_pos)
                Q.append(new_pos)
        self.a[start] = len(self.visited) - v0
        return bounds

    def turn(self, d_idx: int, direction: int = 1) -> tuple[int, Node]:
        d_idx = (d_idx + direction) % 4
        return d_idx, self.D[d_idx]

    @staticmethod
    def num_turns(a: int, b: int) -> int:
        c = abs(a - b)
        return int(c == 3) or c

    def outer(self, r: int, c: int) -> set[Node | None]:
        result = set()
        for dr, dc in self.D:
            if not (0 <= (rr := r + dr) < self._R and 0 <= (cc := c + dc) < self._C):
                return {None}
            result.add(self.regions.get((rr, cc), None))
            self.interior.add((rr, cc))
        return result

    def add_outer(self, start: Node, outers: set[Node | None], s: int) -> None:
        if None in outers:
            return
        outers -= {start}
        if len(outers) > 1:
            return
        pos = outers.pop()
        if all(
            self.exterior.get(node) == pos
            for node in self.interior
            if self.regions[node] != start
        ):
            return
        self.s[pos] += s

    def sides(self, start: Node, bounds: set[Node]) -> None:
        self.interior = set()
        outers = set()
        if len(bounds) <= 2:
            self.s[start] = 4
            for pos in bounds:
                self.exterior[pos] = start
                outers |= self.outer(*pos)
            self.add_outer(start, outers, self.s[start])
            return
        visited = set()
        self.s[start] = 1
        Q = deque([(start, 0)])
        while Q:
            pos, d = Q.popleft()
            r, c = pos
            self.exterior[pos] = start
            outers |= self.outer(*pos)
            if pos == start and d:
                _, (dr, dc) = self.turn(d, -1)
                if (r + dr, c + dc) not in bounds:
                    self.s[start] += self.num_turns(d, 3)
                    self.add_outer(start, outers, self.s[start])
                    return
            if (pos, d) in visited:
                continue
            visited.add((pos, d))
            new_d, (dr, dc) = self.turn(d, -1)
            while (new_pos := (r + dr, c + dc)) not in bounds:
                new_d, (dr, dc) = self.turn(new_d)
            self.s[start] += self.num_turns(d, new_d)
            Q.append((new_pos, new_d))

    def price(self, bulk_discount: bool = False) -> int:
        if bulk_discount:
            b = self.s
        else:
            b = self.p
        return sum(self.a[pos] * b[pos] for pos in self.a)


@aoc_timer
def solve(data: Data, vis: bool = False) -> tuple[int, int]:
    m = Map(G=data)
    if vis:
        view(data)
    for pos, _ in m.items():
        if pos in m.visited:
            continue
        bounds = m.bfs(pos)
        _ = m.sides(pos, bounds)
    return m.price(), m.price(True)


def main() -> None:
    print("AoC 2024\nDay 12")
    data = get_input("input.txt")
    p1, p2 = solve(data, vis=True)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
