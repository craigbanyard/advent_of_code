# %% Day 06
from helper import aoc_timer


class Map:
    def __init__(self, path: str) -> None:
        self.path = path
        self.visited = {}
        self.p2 = 0
        self.get_input()

    @aoc_timer
    def get_input(self) -> None:
        D = {
            "^": -1j,
            ">": 1+0j,
            "v": 1j,
            "<": -1+0j,
        }
        self.obs = set()
        with open(self.path) as f:
            for r, line in enumerate(f.read().splitlines()):
                for c, ch in enumerate(line):
                    if ch == "#":
                        self.obs.add(complex(c, r))
                    elif d := D.get(ch):
                        self.d, self.pos = d, complex(c, r)
            self.R, self.C = r + 1, len(line)

    def patrol(
        self,
        d: complex | None = None,
        pos: complex | None = None,
        obs: set[complex] | None = None,
        log: bool = True,
    ) -> None:
        d = d or self.d
        pos = pos or self.pos
        obs = obs or self.obs
        turns = set()
        while 0 <= pos.imag < self.R and 0 <= pos.real < self.C:
            if log and pos not in self.visited:
                self.visited[pos] = (d, pos - d)
            if (new_pos := pos + d) in obs:
                if (d, new_pos) in turns:
                    self.p2 += 1
                    return
                turns.add((d, new_pos))
                d *= 1j
                continue
            pos = new_pos

    @aoc_timer
    def solve(self) -> tuple[int, int]:
        self.patrol()
        for new_obs, (d, pos) in self.visited.items():
            if new_obs == self.pos:
                continue
            self.patrol(d, pos, self.obs | {new_obs}, log=False)
        return len(self.visited), self.p2


def main() -> None:
    print("AoC 2024\nDay 06")
    m = Map("input.txt")
    p1, p2 = m.solve()
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
