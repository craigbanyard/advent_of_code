from helper import aoc_timer
from functools import lru_cache
from typing import Callable


@aoc_timer
def get_input(path: str) -> tuple[dict[complex, bool], list[int | str]]:
    B = {}
    board, instr = open(path).read().split('\n\n')
    for r, line in enumerate(board.splitlines(), start=1):
        for c, tile in enumerate(line, start=1):
            if tile != ' ':
                B[complex(c, r)] = tile == '.'
    instr = instr.replace('R', ' R ').replace('L', ' L ').split()
    return B, [*map(lambda x: int(x) if not x.isalpha() else x, instr)]


def wrap_map(edges: dict[complex, list[complex]],
             edge_map: dict[complex, tuple[complex, bool]]) -> dict[tuple[complex, complex],
                                                                    tuple[complex, complex]]:
    '''Generate a mapping between positions on the edges of a cube.'''
    E = {}
    for edge1, positions in edges.items():
        if edge1 in E:
            continue
        _, d1 = edge1
        edge2, rev = edge_map[edge1]
        _, d2 = edge2
        e2 = sorted(edges[edge2], key=lambda x: x.real + x.imag, reverse=rev)
        for pos in (e1 := sorted(positions, key=lambda x: x.real + x.imag)):
            idx = e1.index(pos)
            E[(pos, d1)] = (e2[idx], d2)
            E[(e2[idx], d2)] = (pos, d1)
    return E


def cube_net_0(B: dict[complex, bool]) -> dict[tuple[complex, complex],
                                               tuple[complex, complex]]:
    '''
    Set the mapping parameters for the sample input cube net.
    Wrapping assumes the map is folded into a cube where the net is
    of the form:

          #        1
        ###  ->  234
          ##       56

    '''
    N = len([k for k in B if k.imag == 1])

    faces = {
        1: [k for k in B if k.imag <= N],
        2: [k for k in B if k.real <= N],
        3: [k for k in B if N < k.real <= 2*N],
        4: [k for k in B if 2*N < k.real <= 3*N and N < k.imag <= 2*N],
        5: [k for k in B if 2*N < k.real <= 3*N and k.imag > 2*N],
        6: [k for k in B if k.real > 3*N]
    }

    edges = {
        (1, -1j): [k for k in faces[1] if k.imag == 1],
        (1, 1): [k for k in faces[1] if k.real == 3*N],
        (1, -1): [k for k in faces[1] if k.real == 2*N + 1],
        (2, -1j): [k for k in faces[2] if k.imag == N + 1],
        (2, 1j): [k for k in faces[2] if k.imag == 2*N],
        (2, -1): [k for k in faces[2] if k.real == 1],
        (3, -1j): [k for k in faces[3] if k.imag == N + 1],
        (3, 1j): [k for k in faces[3] if k.imag == 2*N],
        (4, 1): [k for k in faces[4] if k.real == 3*N],
        (5, 1j): [k for k in faces[5] if k.imag == 3*N],
        (5, -1): [k for k in faces[5] if k.real == 2*N + 1],
        (6, -1j): [k for k in faces[6] if k.imag == 2*N + 1],
        (6, 1): [k for k in faces[6] if k.real == 4*N],
        (6, 1j): [k for k in faces[6] if k.imag == 3*N]
    }

    # Map {e1: (e2, reversed)}
    edge_map = {
        (1, -1j): ((2, -1j), True),
        (1, 1): ((6, 1), True),
        (1, -1): ((3, -1j), False),
        (2, -1j): ((1, -1j), True),
        (2, 1j): ((5, 1j), True),
        (2, -1): ((6, 1j), True),
        (3, -1j): ((1, -1), False),
        (3, 1j): ((5, -1), True),
        (4, 1): ((6, -1j), True),
        (5, 1j): ((2, 1j), True),
        (5, -1): ((3, 1j), True),
        (6, -1j): ((4, 1), True),
        (6, 1): ((1, 1), True),
        (6, 1j): ((2, -1), True)
    }

    return wrap_map(edges, edge_map)


def cube_net_1(B: dict[complex, bool]) -> dict[tuple[complex, complex],
                                               tuple[complex, complex]]:
    '''
    Set the mapping parameters for the sample input cube net.
    Wrapping assumes the map is folded into a cube where the net is
    of the form:

         ##       12
         #   ->   3
        ##       45
        #        6

    '''
    N = len([k for k in B if k.imag == 1]) // 2

    faces = {
        1: [k for k in B if k.real <= 2*N and k.imag <= N],
        2: [k for k in B if k.real > 2*N],
        3: [k for k in B if N < k.imag <= 2*N],
        4: [k for k in B if k.real <= N and 2*N < k.imag <= 3*N],
        5: [k for k in B if k.real > N and 2*N < k.imag <= 3*N],
        6: [k for k in B if k.imag > 3*N]
    }

    edges = {
        (1, -1j): [k for k in faces[1] if k.imag == 1],
        (1, -1): [k for k in faces[1] if k.real == N + 1],
        (2, -1j): [k for k in faces[2] if k.imag == 1],
        (2, 1): [k for k in faces[2] if k.real == 3*N],
        (2, 1j): [k for k in faces[2] if k.imag == N],
        (3, 1): [k for k in faces[3] if k.real == 2*N],
        (3, -1): [k for k in faces[3] if k.real == N + 1],
        (4, -1j): [k for k in faces[4] if k.imag == 2*N + 1],
        (4, -1): [k for k in faces[4] if k.real == 1],
        (5, 1): [k for k in faces[5] if k.real == 2*N],
        (5, 1j): [k for k in faces[5] if k.imag == 3*N],
        (6, 1): [k for k in faces[6] if k.real == N],
        (6, 1j): [k for k in faces[6] if k.imag == 4*N],
        (6, -1): [k for k in faces[6] if k.real == 1]
    }

    # Map {e1: (e2, reversed)}
    edge_map = {
        (1, -1j): ((6, -1), False),
        (1, -1): ((4, -1), True),
        (2, -1j): ((6, 1j), False),
        (2, 1): ((5, 1), True),
        (2, 1j): ((3, 1), False),
        (3, 1): ((2, 1j), False),
        (3, -1): ((4, -1j), False),
        (4, -1j): ((3, -1), False),
        (4, -1): ((1, -1), True),
        (5, 1): ((2, 1), True),
        (5, 1j): ((6, 1), False),
        (6, 1): ((5, 1j), False),
        (6, 1j): ((2, -1j), False),
        (6, -1): ((1, -1j), False),
    }

    return wrap_map(edges, edge_map)


@aoc_timer
def solve(data: tuple[dict[complex, bool], list[int | str]],
          dims: int = 2, net_func: Callable = cube_net_1) -> int:
    B, instr = data
    D = {
        'R': 1j,
        'L': -1j
    }

    if dims == 3:
        E = net_func(B)

    def wrap_2d(pos: complex,
                d: complex) -> tuple[complex, complex | bool, None]:
        '''
        Return the position that wraps around the map from position
        `pos` when travelling in direction `d`. Assumes `pos` is on
        the edge of the map when facing in direction `d`.
        '''
        p = None
        if d == 1 or d == -1:
            board_row = [k for k in B if k.imag == pos.imag]
            f = (max, min)[d == 1]
            p = f(board_row, key=lambda x: x.real)
        elif d == 1j or d == -1j:
            board_col = [k for k in B if k.real == pos.real]
            f = (max, min)[d == 1j]
            p = f(board_col, key=lambda x: x.imag)
        if not B.get(p, False):
            return False, None
        return p, d

    def wrap_3d(pos: complex,
                d: complex) -> tuple[complex, complex | bool, None]:
        '''
        Return the position that wraps around the map from position
        `pos` when travelling in direction `d`. Assumes `pos` is on
        the edge of the map when facing in direction `d`, and that
        the map is folded into a cube.
        '''
        p, dd = E[pos, d]
        if not B.get(p, False):
            return False, None
        return p, -dd

    @lru_cache
    def wrap(pos: complex,
             d: complex,
             dims: int) -> tuple[complex, complex | bool, None]:
        '''Return the relevant wrap for the number of dimensions.'''
        if dims == 2:
            return wrap_2d(pos, d)
        if dims == 3:
            return wrap_3d(pos, d)
        assert False, f'{dims=} unsupported'

    def password(pos: complex, d: complex) -> int:
        '''
        Return the password implied by the position, `pos`, and the
        facing, `d`.
        '''
        P = {
            1: 0,
            1j: 1,
            -1: 2,
            -1j: 3
        }
        return int(1000*pos.imag + 4*pos.real + P[d])

    pos = min([k for k, v in B.items() if v],
              key=lambda x: 1000*x.imag + x.real)
    d = 1

    for move in instr:
        if move in D:
            d *= D[move]
            continue
        for _ in range(move):
            new_pos = pos + d
            if new_pos not in B:
                wpos, wd = wrap(pos, d, dims)
                if not wpos:
                    break
                pos, d = wpos, wd
                continue
            if not B[new_pos]:
                break
            pos = new_pos

    return password(pos, d)


# %% Output
def main() -> None:
    print("AoC 2022\nDay 22")
    data = get_input('input.txt')
    print("Part 1:", solve(data, dims=2))
    print("Part 2:", solve(data, dims=3))


if __name__ == '__main__':
    main()
