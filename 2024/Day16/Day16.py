# %% Day 16
from helper import aoc_timer, Grid, Colours
from collections import defaultdict
from io import StringIO
import math
import heapq
from typing import Iterator

type Data = list[list[str]]


@aoc_timer
def get_input(path: str) -> Data:
    with open(path) as f:
        return [[*line] for line in f.read().splitlines()]


class Maze(Grid):
    type Node = tuple[int, int]
    type DirNode = tuple[Node, int]
    type VisDict = dict[DirNode, DirNode]
    type CostDict = dict[DirNode, int | float]

    D = [
        (0, 1),     # Right
        (1, 0),     # Down
        (0, -1),    # Left
        (-1, 0),    # Up
    ]

    def __init__(self, **kwargs) -> None:
        """Set '.', 'S', and 'E' as traversable nodes."""
        super().__init__(**kwargs)
        self._valid = set(".SE")

    def valid(self, node: Node) -> bool:
        """Determine whether a given node is traversable."""
        r, c = node
        if 0 <= r < self._R and 0 <= c < self._C:
            return self.G[r][c] in self._valid
        return False

    def neighbours(self, node: DirNode) -> Iterator[DirNode]:
        """Return a generator of valid neighbours of the current node."""
        (r, c), d = node
        for turn in [-1, 0, 1]:
            dd = (d + turn) % 4
            dr, dc = self.D[dd]
            if self.valid(((rr := r + dr), (cc := c + dc))):
                yield (rr, cc), dd

    def cost(self, pos: DirNode, new_pos: DirNode) -> int:
        """Cost to move to node, adding 1000 if this includes a (90 degree) turn."""
        *_, d = pos
        *_, dd = new_pos
        return 1000 * (dd != d) + 1

    def djikstra(self, start: DirNode) -> tuple[VisDict, CostDict]:
        """Perform Djikstra's algorithm on the grid."""
        visited = defaultdict(set)
        cost = defaultdict(lambda: math.inf, {start: 0})
        Q = []
        heapq.heappush(Q, (0, start))
        while Q:
            _, pos = heapq.heappop(Q)
            for new_pos in self.neighbours(pos):
                new_cost = cost[pos] + self.cost(pos, new_pos)
                if new_cost == cost[new_pos]:
                    visited[new_pos].add(pos)
                elif new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    visited[new_pos] = {pos}
                    heapq.heappush(Q, (new_cost, new_pos))
        return visited, cost

    def shortest_path(self, end: Node, cost: CostDict) -> tuple[int, DirNode]:
        """
        Return the minimum cost to the end node, as well as the directed end node. Note
        that the puzzle parameters appear to guarantee that two paths of equal minimal
        cost will not reach the end node travelling in different directions. This method
        therefore assumes that the first time we reach the end node, we are travelling
        in the optimal direction.
        """
        min_cost = math.inf
        for (pos, d), c in cost.items():
            if pos == end and c < min_cost:
                end_node = (pos, d)
                min_cost = c
        return min_cost, end_node

    def construct_path(
        self,
        start: DirNode,
        end: DirNode,
        visited: VisDict,
        all_paths: bool = False,
        path: set | None = None,
    ) -> set[DirNode]:
        """
        Return a set of nodes ((r, c), d) that comprise the path(s) from start to end
        implied by the visited dictionary.
        """
        if path is None:
            path = {end}
        if end == start or end not in visited:
            return path
        for idx, pos in enumerate(visited[end]):
            path.add(pos)
            if all_paths or idx == 0:
                self.construct_path(start, pos, visited, all_paths, path)
        return path

    def visualise_path(
        self,
        path: set[DirNode],
        start: Node,
        end: Node,
        directional: bool = True,
    ) -> str:
        """Return a string representation of the path provided as the argument."""
        grid = StringIO()
        colours = [Colours.BOLD, Colours.fg.CYAN]
        markers = ">v<^" if directional else "OOOO"
        for r in range(self._R):
            for c in range(self._C):
                if (r, c) == start:
                    grid.write(Colours.highlight("S", colours))
                    continue
                if (r, c) == end:
                    grid.write(Colours.highlight("E", colours))
                    continue
                for d in range(4):
                    if ((r, c), d) in path:
                        grid.write(Colours.highlight(markers[d], colours))
                        break
                else:
                    grid.write(self.G[r][c])
            grid.write("\n")
        return grid.getvalue()

    @staticmethod
    def distinct_tiles(path: set[DirNode]) -> set[Node]:
        """
        Return a set of distinct tiles (nodes without direction component) in the
        supplied path.
        """
        return {(r, c) for (r, c), _ in path}


@aoc_timer
def solve(data: Data) -> tuple[int, int]:
    m = Maze(G=data)
    start, end = next(m.where("S")), next(m.where("E"))
    start_dir_node = (start, 0)
    visited, cost = m.djikstra(start_dir_node)

    p1, end_dir_node = m.shortest_path(end, cost)
    path = m.construct_path(start_dir_node, end_dir_node, visited)
    print(m.visualise_path(path, start, end))

    all_paths = m.construct_path(start_dir_node, end_dir_node, visited, True)
    p2 = len(m.distinct_tiles(all_paths))
    print(m.visualise_path(all_paths, start, end, directional=False))

    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 16")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
