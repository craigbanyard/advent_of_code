# %% Day 22
from helper import aoc_timer
from collections import defaultdict, deque


@aoc_timer
def get_input(path: str) -> list[int]:
    with open(path) as f:
        return [*map(int, f.read().splitlines())]


def evolve(n: int) -> int:
    n ^= (n << 6) & 0xFFFFFF
    n ^= (n >> 5) & 0xFFFFFF
    return n ^ (n << 11) & 0xFFFFFF


@aoc_timer
def solve(data: list[int], t: int = 2000) -> tuple[int, int]:
    p1 = 0
    prices = defaultdict(int)
    for n in data:
        changes = deque([], maxlen=4)
        seen = set()
        p = n % 10
        for _ in range(t):
            n = evolve(n)
            q = n % 10
            changes.append(q - p)
            p = q
            if len(changes) == 4 and (c := tuple(changes)) not in seen:
                seen.add(c)
                prices[c] += q
        p1 += n
    return p1, max(prices.values())


def main() -> None:
    print("AoC 2024\nDay 22")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
