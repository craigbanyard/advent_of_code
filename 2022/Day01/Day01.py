from helper import aoc_timer


@aoc_timer
def get_input(path) -> list[list[int]]:
    return [list(map(int, elf.splitlines()))
            for elf in open(path).read().split('\n\n')]


@aoc_timer
def solve(data: list[list[int]], n: int) -> int:
    totals = map(sum, data)
    return sum(sorted(totals, reverse=True)[:n])


# %% Output
def main() -> None:
    print("AoC 2022\nDay 01")
    data = get_input('input.txt')
    print("Part 1:", solve(data, n=1))
    print("Part 2:", solve(data, n=3))


if __name__ == '__main__':
    main()
