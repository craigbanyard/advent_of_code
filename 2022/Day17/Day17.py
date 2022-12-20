from helper import aoc_timer, Colours
import itertools as it
from typing import Iterable


class Rock:
    def __init__(self, points: set[complex]) -> None:
        self.points = points
        self.left: int = int(min(self.points, key=lambda x: x.real).real)
        self.right: int = int(max(self.points, key=lambda x: x.real).real)
        self.bottom: int = int(min(self.points, key=lambda x: x.imag).imag)
        self.top: int = int(max(self.points, key=lambda x: x.imag).imag)

    def __repr__(self) -> str:
        '''
        Return a padded string representation of the Rock (one space in
        all directions surrounding the Rock). The Rock is oriented with
        its top edge as its maximum point in the imaginary plane. For
        this reason, we reverse the output before returning.
        '''
        result = []
        for r in range(self.bottom - 1, self.top + 2):
            line = ''
            for c in range(self.left - 1, self.right + 2):
                point = complex(c, r)
                if point in self.points:
                    line += '#'
                else:
                    line += '.'
            result.append(line)
        return '\n'.join(result[::-1])

    def __eq__(self, __o: type['Rock']) -> bool:
        '''Determine whether the Rock is equal to another.'''
        return self.points == __o.points

    def __and__(self, __o: type['Rock'] | set) -> set:
        '''Define the intersection of the Rock and another.'''
        match __o:
            case set():
                return self.points & __o
        return self.points & __o.points

    def __contains__(self, point: complex) -> bool:
        '''Determine whether a given point lies withing the Rock.'''
        return point in self.points

    def move(self, d: complex) -> type['Rock']:
        '''
        Return a new Rock that is a copy of the Rock, but shifted in
        direction d.
        '''
        return Rock(set(p + d for p in self.points))


class Cave:
    LPAD = 2
    BPAD = 4j
    LWALL = -1
    RWALL = 7
    FLOOR = 0

    def __init__(self, data: str, colour: bool = False) -> None:
        self.data = data
        self.colour = colour
        self.jet: Iterable[str] = it.cycle(self.data)
        self.jet_count: int = 0
        self.rock_count: int = 0
        self.cave: set = set()
        self.high: complex = 0j
        self.highs: dict = {}
        self.state: dict = {}
        self.jet_cycle = len(self.data)
        self.rock_cycle: int = 5
        r1: Rock = Rock({0, 1, 2, 3})
        r2: Rock = Rock({1, 1j, 1+1j, 2+1j, 1+2j})
        r3: Rock = Rock({0, 1, 2, 2+1j, 2+2j})
        r4: Rock = Rock({0, 1j, 2j, 3j})
        r5: Rock = Rock({0, 1, 1j, 1+1j})
        self.rocks: Iterable[Rock] = it.cycle([r1, r2, r3, r4, r5])
        self.rock_map: dict = {r: set() for r in range(self.rock_cycle)}
        self.curr: Rock = r1

    def __repr__(self) -> str:
        '''
        Return a string representation of the Cave. The Cave extends
        vertically upwards in the imaginary plane from the floor at 0j.
        For this reason, we reverse the output before returning.
        '''
        R = {
            0: Colours.fg.YELLOW,
            1: Colours.fg.LIGHTCYAN,
            2: Colours.fg.PURPLE,
            3: Colours.fg.LIGHTBLUE,
            4: Colours.fg.LIGHTGREEN
        }
        result = []
        for r in range(self.curr.top + 1):
            line = ''
            for c in range(self.LWALL, self.RWALL + 1):
                if r == self.FLOOR and c in (self.LWALL, self.RWALL):
                    line += '+'
                    continue
                pos = complex(c, r)
                if pos.imag == self.FLOOR.imag:
                    line += '-'
                elif pos.real in (self.LWALL, self.RWALL):
                    line += '|'
                elif pos in self.cave:
                    if not self.colour:
                        line += '#'
                        continue
                    for idx in range(self.rock_cycle):
                        if pos in self.rock_map[idx]:
                            line += f'{R[idx]}#{Colours.ENDC}'
                            break
                elif pos in self.curr:
                    line += '@'
                else:
                    line += '.'
            result.append(line)
        return '\n'.join(result[::-1])

    def spawn_rock(self) -> None:
        '''Spawn a new Rock at the top of the Cave.'''
        self.rock_count += 1
        self.curr = next(self.rocks)
        self.curr = self.curr.move(self.LPAD + self.BPAD + self.high)

    def blocked(self, rock: Rock) -> bool:
        '''Determine whether the given rock is in a valid position.'''
        if rock & self.cave:
            return True
        if self.FLOOR >= rock.bottom:
            return True
        return self.LWALL >= rock.left or self.RWALL <= rock.right

    def apply_movement(self, d: complex) -> Rock:
        '''
        Return a new Rock that has been shifted by d if that would
        result in a valid Rock position.
        '''
        new_pos = self.curr.move(d)
        if not self.blocked(new_pos):
            return new_pos
        return self.curr

    def apply_jet(self) -> Rock:
        '''Return a new Rock with one unit of the gas jet applied.'''
        self.jet_count += 1
        dx = {'<': -1, '>': 1}[next(self.jet)]
        return self.apply_movement(dx)

    def apply_gravity(self) -> Rock:
        '''Return a new Rock with one unit of gravity applied.'''
        dy = -1j
        return self.apply_movement(dy)

    def fall(self) -> None:
        '''
        Alternate between applying gas jets and gravity until the
        current Rock comes to rest.
        '''
        while True:
            self.curr = self.apply_jet()
            new_pos = self.apply_gravity()
            if new_pos == self.curr:
                self.cave |= self.curr.points
                rock_idx = self.rock_count % self.rock_cycle
                self.rock_map[rock_idx] |= self.curr.points
                self.high = max(self.high.imag, self.curr.top) * 1j
                break
            self.curr = new_pos
        self.highs[self.rock_count] = int(self.high.imag)

    def simulate(self, max_steps: int) -> None:
        '''Simulate continuously falling Rocks up to a given maximum.'''
        for _ in range(max_steps):
            if self.detect_cycle(max_steps):
                break
            self.spawn_rock()
            self.fall()

    def detect_cycle(self, max_steps: int) -> bool:
        '''
        Determine whether the current state (jet index, rock index)
        has been seen before. If it has, and a full cycle has been
        detected, save the predicted final height after the maximum
        number of steps and return True. Otherwise, return False.
        '''
        state = (
            self.jet_count % self.jet_cycle,
            self.rock_count % self.rock_cycle,
        )
        if state in self.state:
            cnt, h = self.state[state]
            d, m = divmod(max_steps - self.rock_count, self.rock_count - cnt)
            if m == 0:
                predicted_height = self.high + (self.high - h) * d
                self.highs[max_steps] = int(predicted_height.imag)
                return True
        self.state[state] = self.rock_count, self.high
        return False


@aoc_timer
def get_input(path: str) -> str:
    return open(path).read().strip()


@aoc_timer
def solve(data: str, max_steps: int) -> int:
    C = Cave(data)
    C.simulate(max_steps)
    return C.highs[max_steps]


# %% Output
def main() -> None:
    print("AoC 2022\nDay 17")
    data = get_input('input.txt')
    print("Part 1:", solve(data, max_steps=2022))
    print("Part 2:", solve(data, max_steps=1000000000000))


if __name__ == '__main__':
    main()
