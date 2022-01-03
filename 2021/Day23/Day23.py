from helper import aoc_timer
from collections import defaultdict, deque
import heapq
import math
import os
import re


A, B, C, D, E = 'ABCD.'
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
def get_input(path):
    '''Return the base starting position of the rooms for part 1.'''
    start = re.findall(r'\w+', open(path).read())
    rooms = []
    for idx in range(len(ROOMS)):
        rooms.append(deque([start[idx], start[idx + 4]]))
    return rooms


def extend_input(data, part2=False):
    '''Return the extended starting position of the rooms for part 2.'''
    if not part2:
        return data
    data = [list(r) for r in data]
    for idx in range(len(ROOMS)):
        data[idx][1:1] = [EXTENSION[idx], EXTENSION[idx + 4]]
    return [deque(r) for r in data]


def mutable(state):
    '''Return a tuple of mutable elements.'''
    hall, rooms = state
    return list(hall), [deque(r) for r in rooms]


def immutable(state):
    '''Return a tuple of immutable elements.'''
    hall, rooms = state
    return tuple(hall), tuple(tuple(x) for x in rooms)


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
        if any(x != E for x in hall[a:b]):
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
        if amp == E:
            continue
        if (res := can_move_home(state, idx, amp, room_size, True)):
            cost, home_idx = res
            new_hall = list(hall)
            new_hall[idx] = E
            _, new_rooms = mutable(([], rooms))
            new_rooms[home_idx].append(amp)
            yield immutable((new_hall, new_rooms)), cost
    # Move from room to hall (or straight home)
    for idx, room in enumerate(rooms):
        if not room:
            continue
        if is_home(idx, rooms):
            continue
        amp = room.popleft()
        if (res := can_move_home((hall, rooms), idx, amp, room_size)):
            cost, home_idx = res
            _, new_rooms = mutable(([], rooms))
            new_rooms[home_idx].append(amp)
            yield immutable((hall, new_rooms)), cost
        # Move from room to unblocked free hall space
        for hall_idx in HALL_IDX:
            if hall[hall_idx] != E:
                continue
            curr_idx = 2 * (idx + 1)
            if hall_idx < curr_idx:
                a, b = hall_idx, curr_idx
            else:
                a, b = curr_idx + 1, hall_idx + 1
            if any(x != E for x in hall[a:b]):
                continue
            new_hall = list(hall)
            new_hall[hall_idx] = amp
            dist = (room_size - len(room)) + abs(hall_idx - curr_idx)
            yield immutable((new_hall, rooms)), COST[amp] * dist
        room.appendleft(amp)


def h_null(_):
    '''A* heuristic: None - becomes Djikstra.'''
    return 0


def h_amp_in_hall(state):
    '''A* heuristic: Number of amphipods in the hallway.'''
    hall, _ = state
    return len([x for x in hall if x != E])


def h_cost_home_hall(state):
    '''A* heuristic: Cost to home from hallway only (ignoring collisions).'''
    hall, _ = state
    return sum([COST[amp] * (abs(ROOM_POS[amp] - idx) + 1)
                for idx, amp in enumerate(hall) if amp != E])


def h_cost_home(state):
    '''A* heuristic: Cost to home (ignoring collisions and walls).'''
    _, rooms = state
    room_cost = sum([COST[amp] * (abs(ROOM_POS[amp] - 2 * (idx + 1)))
                     for idx, room in enumerate(rooms) for amp in room])
    return h_cost_home_hall(state) + room_cost


def show(state, room_size):
    '''Return a string representation of the state.'''
    hall, rooms = mutable(state)
    res = []
    res.append('#############')
    res.append(f"#{''.join(hall)}#")
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
def Day23(data, part2=False, h=h_null):
    hall = [E for _ in range(11)]
    rooms = extend_input(data, part2)
    room_size = len(rooms[0])
    goal_rooms = [deque([room for _ in range(room_size)]) for room in ROOMS]
    goal = immutable((hall, goal_rooms))
    start = immutable((hall, rooms))

    cost = defaultdict(lambda: math.inf, {start: 0})
    prev = {}
    heapq.heappush(Q := [], (0, start))
    iters = 0

    # A* search
    while Q:
        _, state = heapq.heappop(Q)
        if state == goal:
            break
        for new_state, energy_cost in neighbours(state, room_size):
            new_cost = cost[state] + energy_cost
            if new_cost < cost[new_state]:
                cost[new_state] = new_cost
                prev[new_state] = state
                priority = new_cost + h(new_state)
                heapq.heappush(Q, (priority, new_state))
        iters += 1

    # Visualisation
    if (path := construct_path(prev, start, goal)):
        out_file = f'{os.getcwd()}\\Outputs\\part{[1, 2][part2]}.txt'
        with open(out_file, 'w') as f:
            vis = f'{h.__doc__}\n'
            vis += f'States explored: {iters:,}\n'
            vis += visualise(path, cost, room_size)
            f.write(vis)

    return cost[goal]


# %% Output
def main():
    print("AoC 2021\nDay 23")
    data = get_input('input.txt')
    print("Part 1:", Day23(data, part2=False, h=h_cost_home))
    print("Part 2:", Day23(data, part2=True, h=h_null))


if __name__ == '__main__':
    main()
