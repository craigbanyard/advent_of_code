from helper import aoc_timer
from collections import deque
import re


@aoc_timer
def get_input(path: str) -> list:
    return [tuple(map(int, re.findall(r'\d+', line)))
            for line in open(path).read().splitlines()]


def ceildiv(a: int, b: int) -> int:
    '''Perform ceiling division of a by b.'''
    return -(a // -b) if b else 0


@aoc_timer
def solve(data: list[tuple[int]], time_limit: int = 24,
          part2: bool = False) -> int:

    def prune(state: tuple[int], visited: dict[tuple[int], int],
              best: int) -> bool:
        '''Determine whether to prune the current branch early.'''
        _, _, _, d, _, _, _, s, t = state
        if t <= 0:
            return True
        if state in visited:
            return True
        m = t*(t - 1)//2 + d*t
        if m + s < best:
            return True
        return False

    def bfs(start: tuple[int], blueprint: list[int]) -> int:
        '''
        Perform BFS on a blueprint to determine the maximum number of
        geodes that can be cracked. Considers the next robot that can
        be built as a step rather than single timesteps. This reduces
        the search space considerably.
        '''
        best = 0
        visited = {}
        u, v, w, x, y, z = blueprint
        ORE = max(v, w, y)
        Q = deque([(start)])
        while Q:
            state = Q.popleft()
            a, b, c, d, p, q, r, s, t = state
            if s > best:
                best = s
            if prune(state, visited, best):
                continue
            visited[state] = s
            if t < 2:
                # No use building a robot at this stage
                Q.append((a, b, c, d, p+a, q+b, r+c, s+d, 0))
                continue
            if a < ORE and t > 2:
                # Try to build an ore robot
                dt = min(t - 1, max(0, ceildiv(u - p, a)))
                dr = 1 if p + a*dt >= u else 0
                dt += 1
                Q.append((a+dr, b, c, d, p+dt*a-u, q+dt*b, r+dt*c, s+dt*d, t-dt))
            if b < x and t > 2:
                # Try to build a clay robot
                dt = min(t - 1, max(0, ceildiv(v - p, a)))
                dr = 1 if p + a*dt >= v else 0
                dt += 1
                Q.append((a, b+dr, c, d, p+dt*a-v, q+dt*b, r+dt*c, s+dt*d, t-dt))
            if c < z and b > 0 and t > 2:
                # Try to build an obsidian robot
                dt = min(t - 1, max(0, ceildiv(w - p, a), ceildiv(x - q, b)))
                dr = 1 if p + a*dt >= w and q + b*dt >= x else 0
                dt += 1
                Q.append((a, b, c+dr, d, p+dt*a-w, q+dt*b-x, r+dt*c, s+dt*d, t-dt))
            if c > 0:
                # Try to build a geode robot
                dt = min(t - 1, max(0, ceildiv(y - p, a), ceildiv(z - r, c)))
                dr = 1 if p + a*dt >= y and r + c*dt >= z else 0
                dt += 1
                Q.append((a, b, c, d+dr, p+dt*a-y, q+dt*b, r+dt*c-z, s+dt*d, t-dt))
        return best

    # (ore_robots, clay_robots, obsidian_robots, geode_robots,
    #  ore, clay, obsidian, geodes, time)
    start = (1, 0, 0, 0, 0, 0, 0, 0, time_limit)
    p1, p2 = 0, 1
    for idx, *blueprint in data:
        best = bfs(start, blueprint)
        p1 += idx * best
        p2 *= best
    return (p1, p2)[part2]


# %% Output
def main() -> None:
    print("AoC 2022\nDay 19")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data[:3], time_limit=32, part2=True))


if __name__ == '__main__':
    main()
