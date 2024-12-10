# %% Day 09
from helper import aoc_timer
import itertools as it
import numpy as np


@aoc_timer
def get_input(path: str) -> list[int]:
    with open(path) as f:
        return [int(n) for n in f.read().strip()]


def build(data: list[int]) -> tuple[np.ndarray, np.ndarray, list, list]:
    blocks = sum(data)
    disk = np.full(blocks, -1, dtype="int64")
    idx = 0
    files, gaps = data[::2], data[1::2]
    for (fid, size), gap in it.zip_longest(enumerate(files), gaps):
        files[fid] = [size, idx]
        disk[idx : (idx := idx + size)] = fid
        if gap is not None:
            gaps[fid] = [gap, idx]
            idx += gap
    return disk, disk.copy(), files, gaps


def move_blocks(disk: np.ndarray) -> np.ndarray:
    tail = disk[disk >= 0][::-1]
    (gaps,) = (disk[:tail.size] < 0).nonzero()
    disk[gaps] = tail[:gaps.size]
    disk[tail.size:] = -1
    return disk


def move_files(disk: np.ndarray, files: list[int], gaps: list[int]) -> np.ndarray:
    for fid, (f_size, f_idx) in [*enumerate(files)][::-1]:
        for idx, (g_size, g_idx) in enumerate(gaps):
            if f_idx <= g_idx:
                break
            if f_size <= g_size:
                disk[g_idx : (g_idx := g_idx + f_size)] = fid
                disk[f_idx : f_idx + f_size] = -1
                gaps[idx] = [g_size - f_size, g_idx]
                break
    return disk


def checksum(disk: np.ndarray) -> int:
    return (np.maximum(disk, 0) * np.arange(disk.size)).sum()


def view(disk: np.ndarray) -> str:
    return "".join(disk.astype(str)).replace("-1", ".")


@aoc_timer
def solve(data: list[int]) -> int:
    d, e, f, g = build(data)
    p1, p2 = map(checksum, [move_blocks(d), move_files(e, f, g)])
    return p1, p2


def main() -> None:
    print("AoC 2024\nDay 09")
    data = get_input("input.txt")
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
