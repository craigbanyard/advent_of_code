from helper import aoc_timer
from collections import deque


@aoc_timer
def get_input(path: str) -> list[int]:
    return [*map(int, open(path))]


@aoc_timer
def solve(data: list[int], key: int = 1, t: int = 1) -> int:
    data = [*enumerate(x * key for x in data)]
    D = deque(data)
    for _ in range(t):
        for idx, n in data:
            D.rotate(-D.index((idx, n)))
            _, nn = D.popleft()
            D.rotate(-nn)
            D.appendleft((idx, n))
    D = deque([n for _, n in D])
    D.rotate(-D.index(0))
    return sum(D[idx % len(data)] for idx in [1000, 2000, 3000])


# %% Output
def main() -> None:
    print("AoC 2022\nDay 20")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, key=811589153, t=10))


if __name__ == '__main__':
    main()
