# %% Day 06
from helper import aoc_timer


class Map:
    def __init__(self, path: str) -> None:
        self.path = path
        self.visited = set()
        self.get_input()

    @aoc_timer
    def get_input(self) -> None:
        D = {
            "^": -1j,
            ">": 1+0j,
            "v": 1j,
            "<": -1+0j,
        }
        self.W = set()
        self.R = 0
        with open(self.path) as f:
            for r, line in enumerate(f.read().splitlines()):
                self.R += 1
                for c, ch in enumerate(line):
                    if ch == "#":
                        self.W.add(complex(c, r))
                    elif (s := D.get(ch)):
                        self.d, self.pos = s, complex(c, r)
            self.C = len(line)

    def patrol(self, walls: set[complex] | None = None, log: bool = True) -> bool:
        walls = walls or self.W.copy()
        hits = set()
        while 0 <= self.pos.imag < self.R and 0 <= self.pos.real < self.C:
            if log:
                self.visited.add(self.pos)
            if (pos := self.pos + self.d) in walls:
                if (self.d, pos) in hits:
                    return True
                hits.add((self.d, pos))
                self.d *= 1j
                continue
            self.pos = pos
        return False

    @aoc_timer
    def solve(self) -> tuple[int, int]:
        d, pos = self.d, self.pos
        self.patrol()
        p2 = 0
        for p in self.visited:
            self.d, self.pos = d, pos
            p2 += self.patrol(self.W | {p}, log=False)
        return len(self.visited), p2


def main() -> None:
    print("AoC 2024\nDay 06")
    m = Map("input.txt")
    p1, p2 = m.solve()
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
