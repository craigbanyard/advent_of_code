# %% Day 24
from helper import aoc_timer
from collections import deque
import itertools as it
from operator import and_, or_, xor
from typing import Callable

type Wires = dict[str, int]
type Gates = dict[str, tuple[Callable, str, str]]


class System:
    def __init__(self, *, path: str = "", x: int = 0, y: int = 0) -> None:
        self.path = path
        if self.path:
            self.get_input()
            self.read_bits()
            return
        self.x = x
        self.y = y
        self.z = x + y
        self.bits = max(map(int.bit_length, (x, y)))
        self.set_wires()
        self.set_gates()

    def __repr__(self) -> str:
        return f"x={self.x}, y={self.y}\n" + "\n".join(
            f"{a} {f.__name__.upper().removesuffix("_")} {b} -> {c}"
            for c, (f, a, b) in self.gates.items()
        )

    @staticmethod
    def parse_wires(w: str) -> Wires:
        return {k: int(v) for k, v in [line.split(": ") for line in w.splitlines()]}

    @staticmethod
    def parse_gates(g: str) -> Gates:
        F = {"AND": and_, "OR": or_, "XOR": xor}
        return {c: (F[f], a, b) for a, f, b, _, c in [*map(str.split, g.splitlines())]}

    @aoc_timer
    def get_input(self) -> None:
        with open(self.path) as f:
            w, g = f.read().split("\n\n")
        self.wires = self.parse_wires(w)
        self.gates = self.parse_gates(g)

    def read_bits(self) -> None:
        registers = {"x": 0, "y": 0}
        self.bits = 0
        for k, v in self.wires.items():
            r, idx = k[0], int(k[1:])
            self.bits = max(self.bits, idx + 1)
            registers[r] |= (v << idx)
        self.x = registers["x"]
        self.y = registers["y"]
        self.z = self.x + self.y

    def set_wires(self) -> None:
        self.wires = {}
        for n, r in zip([self.x, self.y], ["x", "y"]):
            self.wires |= {
                f"{r}{idx:02d}": int(b)
                for idx, b in enumerate(f"{n:0{self.bits}b}"[::-1])
            }

    def set_gates(self) -> None:
        self.gates = {"z00": (xor, "x00", "y00"), "c01": (and_, "x00", "y00")}
        if self.bits < 2:
            self.gates["z01"] = (and_, "c01", "c01")
            return
        for idx in range(1, self.bits):
            m = f"{idx:02d}"
            n = f"{(idx + 1):02d}"
            self.gates[f"m{m}"] = (xor, f"x{m}", f"y{m}")
            self.gates[f"a{n}"] = (and_, f"x{m}", f"y{m}")
            self.gates[f"z{m}"] = (xor, f"m{m}", f"c{m}")
            self.gates[f"b{n}"] = (and_, f"m{m}", f"c{m}")
            self.gates[f"c{n}"] = (or_, f"a{n}", f"b{n}")
        self.gates[f"z{n}"] = (or_, f"a{n}", f"b{n}")
        self.gates.pop(f"c{n}", None)

    @aoc_timer
    def add(self) -> int:
        result = 0
        Q = deque(self.gates.items())
        while Q:
            key = Q.popleft()
            c, (f, a, b) = key
            if (p := self.wires.get(a)) is None or (q := self.wires.get(b)) is None:
                Q.append(key)
                continue
            r = f(p, q)
            if c[0] == "z":
                result |= (r << int(c[1:]))
            self.wires[c] = r
        return result

    def aligned(self) -> bool:
        return self.z == self.add()

    def validate(self) -> bool:
        n = 100
        for x in range(n):
            for y in range(x, n):
                self.__init__(x=x, y=y)
                assert self.aligned(), f"{self.x=}, {self.y=}"
        return True

    @aoc_timer
    def swap(self) -> str:
        """By inspection of input versus correctly generated gates."""
        swaps = [("shh", "z21"), ("dtk", "vgs"), ("dqr", "z33"), ("pfw", "z39")]
        return ",".join(sorted(it.chain(*swaps)))


def main() -> None:
    print("AoC 2024\nDay 24")
    system = System(path="input.txt")
    print("Part 1:", system.add())
    print("Part 2:", system.swap())


if __name__ == "__main__":
    main()
