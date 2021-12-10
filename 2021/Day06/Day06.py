from helper import aoc_timer
from collections import Counter, deque
import numpy as np


@aoc_timer
def get_input(path: str) -> Counter[int]:
    return Counter(map(int, [*open(path).read().split(',')]))


@aoc_timer
def Day06(data: Counter[int], days: int) -> int:
    '''
    Main solution using deque for efficient pops/appends.
    popleft() used to decrement all fish timers by 1 day.
    append() used to create a new fish with a timer of 8.
    '''
    fish = deque([data[i] for i in range(9)], maxlen=9)
    for _ in range(days):
        births = fish.popleft()
        fish[6] += births
        fish.append(births)
    return sum(fish)


@aoc_timer
def solve(data: Counter[int], days: int) -> int:
    """
    Alternative solution using matrix exponentiation of the
    transition matrix multiplied by the fish counts vector.
    """
    f = np.array([data[i] for i in range(9)], dtype=object)

    t = np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=object)

    return np.dot(np.linalg.matrix_power(t, days), f).sum()


# %% Output
def main():
    print("AoC 2021\nDay 06")
    data = get_input('input.txt')
    print("Part 1:", Day06(data, 80))
    print("Part 2:", Day06(data, 256))


if __name__ == '__main__':
    main()
