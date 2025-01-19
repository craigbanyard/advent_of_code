# %% Day 23
from helper import aoc_timer
from collections import defaultdict
import itertools as it

type Data = dict[str, set[str]]


@aoc_timer
def get_input(path: str) -> Data:
    network = defaultdict(set)
    with open(path) as f:
        for line in f.read().splitlines():
            a, b = line.split("-")
            network[a].add(b)
            network[b].add(a)
    return network


def networks(data: Data, hint: str, n: int, prune: bool = False) -> set[frozenset[str]]:
    nets = set()
    for root, connections in data.items():
        for computers in it.combinations(connections, n - 1):
            if not any([c.startswith(hint) for c in (root, *computers)]):
                continue
            connected = True
            for a, b in it.combinations(computers, 2):
                if a not in data[b]:
                    connected = False
                    break
            if connected:
                nets.add(frozenset((root, *computers)))
        if prune and len(nets) > 1:
            break
    return nets


@aoc_timer
def solve(data: Data, hint: str = "t", n: int = 3) -> tuple[int, str]:
    p1 = len(networks(data, hint, n))
    p2 = None
    for n in range(n + 1, len(data)):
        nets = networks(data, hint, n, prune=True)
        if (count := len(nets)) == 0:
            return p1, p2
        if count == 1:
            p2 = ",".join(sorted(nets.pop()))


def main() -> None:
    print("AoC 2024\nDay 23")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
