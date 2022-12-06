from helper import aoc_timer


@aoc_timer
def get_input(path: str) -> str:
    return open(path).read().strip()


@aoc_timer
def solve(data: str, chunk_size: int) -> int:
    for idx in range(len(data) - chunk_size):
        chunk = data[idx:idx+chunk_size]
        if len(set(chunk)) == chunk_size:
            return idx + chunk_size
    return 0


# %% Output
def main() -> None:
    print("AoC 2022\nDay 06")
    data = get_input('input.txt')
    print("Part 1:", solve(data, chunk_size=4))
    print("Part 2:", solve(data, chunk_size=14))


if __name__ == '__main__':
    main()
