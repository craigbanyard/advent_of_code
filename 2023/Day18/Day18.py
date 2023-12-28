# %% Day 18
from helper import aoc_timer
from typing import Iterator


@aoc_timer
def get_input(path: str) -> Iterator[tuple[str, int, str, int]]:
    for line in open(path).read().splitlines():
        d, n, h = line.split()
        h = h.strip('(#)')
        yield d, int(n), 'RDLU'[int(h[-1])], int(h[:-1], 16)


def area(vertices: list[complex], b: int) -> int:
    '''
    Require number of interior (i) plus boundary (b) points.

    Shoelace formula:
      A = Σ[yᵢ(xᵢ₋₁ - xᵢ₊₁)]/2
        i ∈ [1, n]
        n = number of vertices

    Pick's theorem:
      A = i + b/2 - 1
        A = area (derived via shoelace formula above)
        i = number of internal points
        b = number of boundary points
        ⇒ (i + b) = A + b/2 + 1

    '''
    a = 0
    for idx, v in enumerate(vertices[1:-1], start=1):
        a += v.imag * (vertices[idx - 1].real - vertices[idx + 1].real)
    return int(a//2 + b//2 + 1)


@aoc_timer
def solve(data: Iterator[tuple[str, int, str, int]]) -> tuple[int]:
    D = {
        'R': 1+0j,
        'D': 0+1j,
        'L': -1+0j,
        'U': 0-1j
    }
    b1 = b2 = 1
    c1 = c2 = 0+0j
    v1,  v2 = [], []
    for d1, n1, d2, n2 in data:
        v1.append((c1 := c1 + n1 * D[d1]))
        v2.append((c2 := c2 + n2 * D[d2]))
        b1 += n1
        b2 += n2
    return area(v1, b1), area(v2, b2)


def main() -> None:
    print("AoC 2023\nDay 18")
    data = get_input('input.txt')
    p1, p2 = solve(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
