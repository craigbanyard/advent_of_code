from helper import aoc_timer
from collections import defaultdict, deque
from copy import deepcopy
import heapq
import math
import re


A, B, C, D = 'ABCD'
ROOMS = [A, B, C, D]
COST = {room: 10 ** idx for idx, room in enumerate(ROOMS)}
EXTENSION = [
    D, C, B, A,
    D, B, A, C
]
HALL_IDX = [0, 1, 3, 5, 7, 9, 10]
ROOM_IDX = [2, 4, 6, 8]
ROOM_POS = {k: v for k, v in zip(ROOMS, ROOM_IDX)}


@aoc_timer
def get_input(path, part2=False):
    start = re.findall(r'\w+', open(path).read())
    rooms = []
    for idx in range(len(ROOMS)):
        rooms.append([start[idx], start[idx + 4]])
        if part2:
            rooms[idx][1:1] = [EXTENSION[idx], EXTENSION[idx + 4]]
    return [deque(r) for r in rooms]


def mutable(state):
    '''Return a tuple of mutable elements.'''
    hall, rooms = state
    return list(hall), [deque(r) for r in rooms]


def immutable(state):
    '''Return a tuple of immutable elements.'''
    hall, rooms = state
    return tuple(hall), tuple(tuple(x) for x in rooms)


def comparable(state):
    '''
    Return a state that can be compared using tuple comparison.
    This is required for adding states to the priority queue.
    '''
    hall, rooms = state
    return tuple('.' if not x else x for x in hall), rooms


def incomparable(state):
    '''Inverse of comparible, return state to its original form.'''
    hall, rooms = state
    return tuple(None if x == '.' else x for x in hall), rooms


def show(state, room_size):
    '''Return a string representation of the state.'''
    hall, rooms = mutable(state)
    res = []
    res.append('#############')
    res.append(f"#{''.join([x if x else '.' for x in hall])}#")
    for idx, room in enumerate(rooms):
        while len(room) < room_size:
            room.appendleft('.')
    for idx, row in enumerate(zip(*rooms)):
        if idx == 0:
            pad = '##'
        else:
            pad = '  '
        res.append(f"{pad}#{'#'.join(row)}#{pad}")
    res.append('  #########')
    return '\n'.join(res)


def is_home(idx, rooms):
    '''Determine whether a room is in the goal state.'''
    return all(occupant == ROOMS[idx] for occupant in rooms[idx])


def can_move_home(state, idx, amp, room_size, from_hall=False):
    '''
    Determine whether an amphipod can move directly home from its
    current position. If it can, return the cost of doing so. If
    it cannot, return False.
    '''
    hall, rooms = state
    home_pos = ROOM_POS[amp]
    home_idx = home_pos // 2 - 1
    target_room = rooms[home_idx]
    if len(target_room) == room_size:
        return False
    if not target_room or all(x == amp for x in target_room):
        if from_hall:
            if idx > home_pos:
                a, b = home_pos, idx
            else:
                a, b = idx + 1, home_pos + 1
            exit = 0
        else:
            current_room = rooms[idx]
            idx = 2 * (idx + 1)
            if idx > home_pos:
                a, b = home_pos, idx + 1
            else:
                a, b = idx, home_pos + 1
            exit = (room_size - len(current_room))
        if any(hall[a:b]):
            return False
        # Can move home, return cost to do so
        hall = abs(home_pos - idx)
        enter = (room_size - len(target_room))
        return COST[amp] * (exit + hall + enter), home_idx
    return False


def neighbours(state, room_size):
    '''
    Return a generator of all states that are one legal move away
    from the given state. Considers three possible move types:
        1. Move from hall directly to home
        2. Move from a starting romm directly to home
        3. Move from a starting room to the hall
    '''
    hall, rooms = mutable(state)
    # Move from hall to home
    for idx, amp in enumerate(hall):
        if not amp:
            continue
        if (ret := can_move_home(state, idx, amp, room_size, True)):
            cost, home_idx = ret
            new_hall = list(hall)
            new_hall[idx] = None
            new_rooms = deepcopy(rooms)
            new_rooms[home_idx].append(amp)
            yield immutable((new_hall, new_rooms)), cost
    # Move from room to hall (or straight home)
    for idx, room in enumerate(rooms):
        if not room:
            continue
        if is_home(idx, rooms):
            continue
        amp = room.popleft()
        if (ret := can_move_home((hall, rooms), idx, amp, room_size)):
            cost, home_idx = ret
            new_rooms = deepcopy(rooms)
            new_rooms[home_idx].append(amp)
            yield immutable((hall, new_rooms)), cost
        # Move from room to unblocked free hall space
        for hall_idx in HALL_IDX:
            if hall[hall_idx]:
                continue
            curr_idx = 2 * (idx + 1)
            if hall_idx < curr_idx:
                a, b = hall_idx, curr_idx
            else:
                a, b = curr_idx + 1, hall_idx + 1
            if any(hall[a:b]):
                continue
            new_hall = list(hall)
            new_hall[hall_idx] = amp
            dist = (room_size - len(room)) + abs(hall_idx - curr_idx)
            yield immutable((new_hall, rooms)), COST[amp] * dist
        room.appendleft(amp)


def h(state):
    '''A* heuristic: number of amphipods in the hallway.'''
    hall, _ = state
    return len([x for x in hall if x])


def construct_path(paths, start, end):
    '''Return a list of states that comprise the path from start to end.'''
    if end not in paths:
        return None
    c = end
    path = [c]
    while c in paths:
        c = paths[c]
        path.append(c)
        if c == start:
            return reversed(path)
    return None


def visualise(path, cost, room_size):
    '''Return a string representation of a path of states.'''
    vis = ''
    for state in path:
        vis += f'\nEnergy: {cost[state]}\n'
        vis += show(state, room_size)
        vis += '\n'
    return vis


@aoc_timer
def Day23(path, part2=False):
    hall = [None for _ in range(11)]
    rooms = get_input(path, part2)
    room_size = len(rooms[0])
    goal_rooms = [deque([room for _ in range(room_size)]) for room in ROOMS]
    goal = immutable((hall, goal_rooms))
    start = immutable((hall, rooms))

    cost = defaultdict(lambda: math.inf, {start: 0})
    prev = {}
    heapq.heappush(Q := [], (0, start))

    # Djikstra
    while Q:
        _, state = heapq.heappop(Q)
        state = incomparable(state)
        if state == goal:
            break
        for new_state, energy_cost in neighbours(state, room_size):
            new_cost = cost[state] + energy_cost
            if new_cost < cost[new_state]:
                cost[new_state] = new_cost
                prev[new_state] = state
                priority = new_cost + h(new_state)
                heapq.heappush(Q, (priority, comparable(new_state)))

    # Visualisation
    path = construct_path(prev, start, goal)
    if path:
        print(visualise(path, cost, room_size))

    return cost[goal]


# %% Output
def main():
    print("AoC 2021\nDay 23")
    path = 'input.txt'
    print("Part 1:", Day23(path, part2=False))
    print("Part 2:", Day23(path, part2=True))


if __name__ == '__main__':
    main()
