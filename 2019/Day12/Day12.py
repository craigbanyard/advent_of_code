from helper import aoc_timer
import numpy as np
import itertools
import re


@aoc_timer
def get_input(path):
    return np.array(
        [
            [int(x) for x in re.findall(r'-?\d+', line)]
            for line in open(path).readlines()
        ],
        dtype=int
    )


@aoc_timer
def Day12(data, part2=False, timesteps=1000):
    # Position and velocity of moons
    pos = data.copy()
    vel = pos * 0
    # Orbital period for each coordinate
    periods_to_find = {c for c in range(data.shape[1])}
    periods_found = {}

    def evolve(pos, vel):
        """Simulate one timestep of motion of the system."""
        for (i, m1), (j, m2) in itertools.combinations(enumerate(pos), 2):
            gravity = np.sign(np.subtract(m2, m1))
            vel[i] += gravity
            vel[j] -= gravity
        pos += vel
        return pos, vel

    def check_cycle(periods_to_find):
        """
        Coordinates are independent!
        When a coordinate's velocity reaches zero, we know it has hit a cycle
        The timestep at which this occurs is that coordinate's return period
        When this has happened for all coordinates, we can then calculate the
        LCM to determine the timestep where all coordinates have zero velocity
        """
        for k in periods_to_find:
            if all(vel[:, k] == 0):
                periods_found[k] = t
        periods_to_find -= periods_found.keys()
        return not periods_to_find

    for t in range(1, timesteps + 1):
        pos, vel = evolve(pos, vel)

        if part2 and check_cycle(periods_to_find):
            return 2 * np.lcm.reduce(
                np.fromiter(periods_found.values(), dtype='int64')
            )

    pot = np.sum(abs(pos), axis=1)
    kin = np.sum(abs(vel), axis=1)
    return np.sum(pot * kin)


# %% Output
def main():
    print("AoC 2019\nDay 12")
    data = get_input('input.txt')
    print("Part 1:", Day12(data, part2=False, timesteps=1000))
    print("Part 2:", Day12(data, part2=True, timesteps=200000))


if __name__ == '__main__':
    main()
