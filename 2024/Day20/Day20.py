# %% Day 20
from helper import aoc_timer, Grid
from collections import deque
import math
import numpy as np
from scipy.ndimage import generic_filter
from typing import Any, Iterator

type Data = list[list[str]]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        return [[*line] for line in f.read().splitlines()]


class Racetrack(Grid):
    type Node = tuple[int, int]
    type CostDict = dict[Node, int | float]

    def __init__(self, **kwargs) -> None:
        """Set '.', 'S', and 'E' as traversable nodes."""
        super().__init__(**kwargs)
        self._valid = set(".SE")

    def valid(self, node: Node, cheat: bool = False) -> bool:
        """Determine whether a given node is traversable."""
        r, c = node
        if 0 <= r < self._R and 0 <= c < self._C:
            return cheat or self.G[r][c] in self._valid
        return False

    def neighbours(self, node: Node, cheat: bool = False) -> Iterator[Node]:
        """Return a generator of valid neighbours (open spaces) of the current node."""
        r, c = node
        for dr, dc in self.D:
            if self.valid(((rr := r + dr), (cc := c + dc)), cheat):
                yield (rr, cc)

    def bfs(
        self,
        start: Any,
        end: Any,
        max_cost: int | float = math.inf,
        cheat: bool = False,
    ) -> CostDict:
        """Perform breadth-first search (BFS) on the grid, optionally cheating."""
        start_nodes = self._init_traversal(start)
        cost = self._init_cost_dict(start_nodes)
        Q = deque([*start_nodes])
        while Q:
            pos = Q.popleft()
            if self._traversal_complete(pos, cost, end, max_cost):
                break
            for new_pos in self.neighbours(pos, cheat):
                new_cost = cost[pos] + self.cost(new_pos)
                if new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    Q.append(new_pos)
        return cost

    def cheat(self, cost: CostDict, duration: int, threshold: int) -> int:
        """
        Determine the number of cheats lasting `duration` steps that will save at least
        `threshold` steps.
        """
        result = 0
        for (r, c), t in cost.items():
            if self.G[r][c] == "E":
                continue
            for (rr, cc), tt in self.bfs((r, c), None, duration, True).items():
                if (rr, cc) not in cost:
                    continue
                if cost[(rr, cc)] - t - tt >= threshold:
                    result += 1
        return result

    def cheat_convolve(self, cost: CostDict, duration: int, threshold: int) -> int:
        """
        Implementation of `cheat` using convolution. Pass a kernel representing all
        positions that can be reached within `duration` steps over the array of costs
        and count occurrences where the cheat will save at least `threshold` steps.
        """
        costs = np.full_like(self.G, np.nan, dtype="float64")
        for pos, t in cost.items():
            costs[pos] = t

        d = duration * 2 + 1
        i, j = np.indices((d, d), sparse=True)
        dists = (abs((i - duration)) + abs((j - duration)))
        kernel = dists <= duration
        dists = dists[kernel].reshape(-1)

        def f(arr: np.ndarray, dists: np.ndarray) -> int:
            return np.count_nonzero(arr - arr[arr.size // 2] - dists >= threshold)

        return generic_filter(
            costs, f, footprint=kernel, mode="constant", extra_arguments=(dists,)
        ).sum(dtype=int)


@aoc_timer
def solve(data: Data, duration: int, threshold: int = 100, conv: bool = True) -> int:
    racetrack = Racetrack(G=data)
    cost = racetrack.bfs("S", "E")
    return (racetrack.cheat, racetrack.cheat_convolve)[conv](cost, duration, threshold)


def main() -> None:
    print("AoC 2024\nDay 20")
    data = get_input("input.txt")
    print("Part 1:", solve(data, 2))
    print("Part 2:", solve(data, 20))


if __name__ == "__main__":
    main()
