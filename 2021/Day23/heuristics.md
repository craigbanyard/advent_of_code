# Advent of Code 2021, Day 23 - Amphipod
## Sensitivity of A* algorithm to choice of heuristic

I have implemented four heuristic functions for my A* search algorithm:

1. None - i.e. perform Djikstra's algorithm instead of A*

```python
def h_null(_):
    '''A* heuristic: None - becomes Djikstra.'''
    return 0
```

2. Amphipods in hallway - the number of amphipods in the hallway

```python
def h_amp_in_hall(state):
    '''A* heuristic: Number of amphipods in the hallway.'''
    hall, _ = state
    return len([x for x in hall if x != E])
```

3. Cost home from hallway - the cost to move all amphipods currently in the hallway directly to their homes, ignoring collisions and room entry restrictions

```python
def h_cost_home_hall(state):
    '''A* heuristic: Cost to home from hallway only (ignoring collisions).'''
    hall, _ = state
    return sum([COST[amp] * (abs(ROOM_POS[amp] - idx) + 1)
                for idx, amp in enumerate(hall) if amp != E])
```


4. Cost home - the cost to move all amphipods directly home from their current positions, ignoring collisions, room entry restrictions and walls between rooms

```python
def h_cost_home(state):
    '''A* heuristic: Cost to home (ignoring collisions and walls).'''
    _, rooms = state
    room_cost = sum([COST[amp] * (abs(ROOM_POS[amp] - 2 * (idx + 1)))
                     for idx, room in enumerate(rooms) for amp in room])
    return h_cost_home_hall(state) + room_cost
```

The impact on the number of states explored and the runtime of the algorithm on both parts is shown below:

| Heuristic | States Explored<br>Part 1 | States Explored<br>Part 2 | Runtime<br>Part 1 | Runtime<br>Part 2 |
|---|--:|--:|--:|--:|
| None | 72,932 | 114,529 | 3.244 | 4.444 |
| Amphipods in hallway | 72,798 | 114,528 | 3.504 | 4.794 |
| Cost home from hallway | 32,663 | 114,715 | 1.616 | 4.878 |
| Cost home | 30,759 | 114,662 | 1.546 | 5.668 |

Heuristic 4 is best overall for part 1, whereas Djikstra (no heuristic) performs best overall on part 2.
