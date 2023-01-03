from helper import aoc_timer
from collections import deque
import heapq
import operator as op
import re
from typing import Callable, Iterator


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


def process_resources(r1: tuple, r2: tuple,
                      operation: Callable = op.add) -> tuple:
    '''Perform element-wise operation on two tuples.'''
    return tuple(operation(a, b) for a, b in zip(r1, r2))


def wait(state: tuple, duration: int = 1) -> tuple:
    '''
    Wait a single timestep without building any new robots.
    '''
    robots, resources, time = state
    for _ in range(duration):
        new_resources = process_resources(robots, resources)
        time += 1
    return (robots, new_resources, time)


def build(state: tuple, blueprint: tuple,
          production_cap: tuple, time_limit: int) -> Iterator:
    '''
    Return a generator of newly built robots (by index), the
    remaining resources after building, and the new time.
    Will never suggest building a robot if this would take the
    production rate for that resource above the maximum required
    per minute (for all robots except geode-cracking robots).
    Subject to the above restriction, increments resources (and
    time) until each new robot can be built.
    If close to the time limit, allow incrementing resources
    without building any additional robots, as these may be
    ineffectual.
    This cuts down on the number of states that need to be
    explored.
    '''
    robots, resources, time = state
    if (time_remaining := time_limit - time) < 2:
        yield wait(state, duration=time_remaining)
        return None
    for idx, robot in enumerate(blueprint):
        if robots[idx] > production_cap[idx] and idx < 3:
            continue
        if any(process_resources(robots, robot, lambda a, b: b and not a)):
            # Cannot possibly build this robot without first building
            # other robots
            continue
        new_time = time
        new_res = resources
        while (any(process_resources(robot, new_res, op.gt))
               and new_time < time_limit - 1):
            # Gather more resources until we can afford this robot
            _, new_res, new_time = wait((robots, new_res, new_time))
        # Build the new robot if possible
        if all(new_res := process_resources(new_res, robot, op.sub)) >= 0:
            add_robot = tuple(1 if r == idx else 0 for r in range(4))
            new_robots = process_resources(robots, add_robot)
        else:
            new_robots = robots
        # Increment time and resources for existing robots
        _, new_res, new_time = wait((robots, new_res, new_time))
        # Yield new state
        yield (new_robots, new_res, new_time)


@aoc_timer
def solve(data: list, time_limit: int = 24, part2: bool = False) -> int:

    def prune(state: tuple, visited: dict, best: int) -> bool:
        '''Determine whether to prune the current branch.'''
        robots, resources, time = state
        if time >= time_limit:
            return True
        if state in visited:
            return True
        geode_robots = robots[-1]
        open_geodes = resources[-1]
        n = time_limit - time
        max_crackable = n * (n - 1) // 2 + geode_robots * n
        if max_crackable + open_geodes < best:
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
            _, resources, time = state
            if resources[-1] > best:
                best = resources[-1]
                print(f'New best: {best} @ minute {time}')
            if prune(state, visited, best):
                continue
            visited[state] = resources[-1]
            for new_state in build(state, blueprint, production_cap, time_limit):
                Q.append((new_state))
        print(f'Geodes: {best}')
        return best

    def djikstra(start: tuple, blueprint: tuple) -> int:
        '''
        Perform Djikstra's algorithm on the blueprint to calculate
        the maximum crackable geodes. Current implementation is
        slower than BFS.
        '''
        best = 0
        visited = {}
        production_cap = tuple(max(r) for r in zip(*blueprint))
        Q = deque([(start)])
        heapq.heappush(Q := [], (0, start))
        while Q:
            _, state = heapq.heappop(Q)
            _, resources, time = state
            if resources[-1] > best:
                best = resources[-1]
                print(f'New best: {best} @ minute {time}')
            if prune(state, visited, best):
                continue
            visited[state] = resources[-1]
            for new_state in build(state, blueprint, production_cap, time_limit):
                _, resources, t = new_state
                priority = tuple(([-r for r in resources[:0:-1]], time_limit - t))
                heapq.heappush(Q, (priority, new_state))
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
