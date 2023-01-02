from helper import aoc_timer
from collections import deque
import re
from typing import Iterator


@aoc_timer
def get_input(path: str) -> list:
    B = []
    for blueprint in open(path).read().splitlines():
        _, *c = [*map(int, re.findall(r'\d+', blueprint))]
        assert len(c) == 6, f'Unexpected blueprint schema: {blueprint}'
        B.append((
            (c[0], 0, 0, 0),
            (c[1], 0, 0, 0),
            (c[2], c[3], 0, 0),
            (c[4], 0, c[5], 0)
        ))
    return B


def buildable(robots: tuple, resources: tuple,
              blueprint: tuple, production_cap: tuple) -> Iterator:
    '''
    Return a generator of buildable robots (by index) and the
    remaining resources after building this robot. Will never
    suggest building a robot if this would take the production
    rate for that resource above the maximum required per
    minute (for all robots except geode-cracking robots).
    '''
    for idx, robot in enumerate(blueprint):
        if robots[idx] > production_cap[idx] and idx < 3:
            break
        remaining = []
        for owned, cost in zip(resources, robot):
            if (r := owned - cost) < 0:
                break
            remaining.append(r)
        else:
            yield idx, tuple(remaining)


def update_resources(r1: tuple, r2: tuple) -> tuple:
    '''Perform element-wise addition on two tuples.'''
    return tuple(a + b for a, b in zip(r1, r2))


@aoc_timer
def solve(data: list, time_limit: int = 24, part2: bool = False) -> int:

    def prune(state: tuple, visited: dict, best: int) -> bool:
        '''Determine whether to prune the current branch.'''
        _, resources, time = state
        if time >= time_limit:
            return True
        if state in visited:
            return True
        geodes = resources[-1]
        if time_limit - time < best - geodes:
            return True
        return False

    def bfs(start: tuple, blueprint: tuple) -> int:
        '''
        Perform BFS on the blueprint to calculate the maximum
        crackable geodes.
        '''
        best = 0
        visited = {}
        production_cap = tuple(max(r) for r in zip(*blueprint))
        Q = deque([(start)])
        while Q:
            state = Q.popleft()
            robots, resources, time = state
            if resources[-1] > best:
                best = resources[-1]
                print(f'New best: {best} @ minute {time}')
            if prune(state, visited, best):
                continue
            visited[state] = resources[-1]
            build_state = robots, resources, blueprint, production_cap
            for new_robot, remain_res in buildable(*build_state):
                new_robots = list(robots)
                new_robots[new_robot] += 1
                new_resources = update_resources(robots, remain_res)
                Q.append((tuple(new_robots), new_resources, time + 1))
            add_resources = update_resources(robots, resources)
            Q.append((robots, add_resources, time + 1))
        print(f'Geodes: {best}')
        return best

    p1, p2 = 0, 1
    # ((robots), (resources), time)
    start = ((1, 0, 0, 0), (0, 0, 0, 0), 0)
    for idx, blueprint in enumerate(data, start=1):
        print(f'Analysing blueprint {idx} of {len(data)}...')
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
