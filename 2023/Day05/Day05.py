# %% Day 05
from helper import aoc_timer


@aoc_timer
def get_input(path: str) -> tuple[list[str], list[list[str]]]:
    seeds_, *maps_ = open(path).read().split('\n\n')
    seeds = seeds_[7:].split()
    maps = [m.splitlines()[1:] for m in maps_]
    return seeds, maps


def sort_map(m: list[str], sort_index: int = 1) -> list[list[int]]:
    result = []
    for rng in m:
        result.append([*map(int, rng.split())])
    return sorted(result, key=lambda x: x[sort_index])


@aoc_timer
def part1(data: tuple[list[str], list[list[str]]]) -> int:
    seeds, maps = data
    S = {s: s for s in map(int, seeds)}
    for m in maps:
        for k, v in S.items():
            for d, s, n in sort_map(m):
                if s <= v < s + n:
                    S[k] = v + (d - s)
                    break
    return min(S.values())


@aoc_timer
def part2(data: tuple[list[str], list[list[str]]],
           threshold : int = 1e9,
           progress: bool = False) -> int:
    seeds, maps = data
    seeds = [*map(int, seeds)]
    S = [range(a, a + b) for a, b in sorted(zip(seeds[::2], seeds[1::2]))]
    M = [*reversed([sort_map(m, sort_index=0) for m in maps])]
    loc = 0
    while True:
        idx = loc
        for m in M:
            for d, s, n in m:
                if idx < d:
                    break
                elif d <= idx < d + n:
                    idx += (s - d)
                    break
        for rng in S:
            if idx in rng:
                return loc
        loc += 1
        if progress and loc % 1e6 == 0:
            print(f'Scanning location: {loc:,}')
        if loc > threshold:
            print(f'Failed to find valid location with threshold: {threshold:,}')
            break
    return None


def main() -> None:
    print("AoC 2023\nDay 05")
    data = get_input('input.txt')
    # data = get_input('sample.txt')
    print("Part 1:", part1(data))
    print("Part 2:", part2(data, progress=True))


if __name__ == '__main__':
    main()
