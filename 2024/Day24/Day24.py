# %% Day 24
from helper import aoc_timer
from collections import deque
from dataclasses import dataclass
from operator import and_, or_, xor
from typing import Iterator


@dataclass
class Gate:
    f_: str
    a: str
    b: str

    def __post_init__(self) -> None:
        self.f = {"AND": and_, "OR": or_, "XOR": xor}[self.f_]
        self.a, self.b = sorted([self.a, self.b])

    def __repr__(self) -> str:
        return f"{self.a} {self.f_} {self.b}"

    def __hash__(self) -> int:
        return hash((self.f_, self.a, self.b))

    def __iter__(self) -> Iterator:
        yield from (self.f_, self.a, self.b)


class System:
    def __init__(self, *, path: str = "", x: int = 0, y: int = 0) -> None:
        if path:
            self.path = path
            self.get_input()
            self.read_bits()
        else:
            self.x = x
            self.y = y
            self.z = x + y
            self.bits = max(map(int.bit_length, (x, y)))
            self.set_wires()
            self.set_gates()
        self.gates_ = self.invert_gates()
        self.errors = set()

    def __repr__(self) -> str:
        return f"x={self.x}, y={self.y}\n" + "\n".join(
            f"{v} -> {k}" for k, v in self.gates.items()
        )

    @staticmethod
    def parse_wires(w: str) -> dict[str, int]:
        return {k: int(v) for k, v in [line.split(": ") for line in w.splitlines()]}

    @staticmethod
    def parse_gates(g: str) -> dict[str, Gate]:
        return {c: Gate(f, a, b) for a, f, b, _, c in [*map(str.split, g.splitlines())]}

    def invert_gates(self) -> dict[Gate, str]:
        return {v: k for k, v in self.gates.items()}

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
        self.gates = {
            "z00": Gate("XOR", "x00", "y00"),
            "c01": Gate("AND", "x00", "y00"),
        }
        if self.bits < 2:
            self.gates["z01"] = Gate("OR", "c01", "c01")
            return
        for idx in range(1, self.bits):
            X, Y, Z, M, C = [f"{r}{idx:02d}" for r in "xyzmc"]
            A, B, C_, Z_ = [f"{r}{(idx + 1):02d}" for r in "abcz"]
            self.gates[M] = Gate("XOR", X, Y)
            self.gates[A] = Gate("AND", X, Y)
            self.gates[Z] = Gate("XOR", M, C)
            self.gates[B] = Gate("AND", M, C)
            self.gates[C_] = Gate("OR", A, B)
        self.gates[Z_] = Gate("OR", A, B)
        self.gates.pop(C_, None)

    @aoc_timer
    def add(self, **kwargs) -> int:
        result = 0
        wires = self.wires.copy()
        Q = deque(self.gates.items())
        while Q:
            c, gate = Q.popleft()
            if (p := wires.get(gate.a)) is None or (q := wires.get(gate.b)) is None:
                Q.append((c, gate))
                continue
            r = gate.f(p, q)
            if c[0] == "z":
                result |= (r << int(c[1:]))
            wires[c] = r
        return result

    def aligned(self) -> bool:
        return self.z == self.add(time=False)

    def swap_outputs(self, a, b) -> None:
        self.errors.update((a, b))
        self.gates[a], self.gates[b] = self.gates[b], self.gates[a]

    def debug_adder(self, idx: int) -> None:
        X, Y, Z = [f"{r}{idx:02d}" for r in "xyz"]
        # x ^ y = m
        m = self.gates_[Gate("XOR", X, Y)]
        # x & y = a
        a = self.gates_[Gate("AND", X, Y)]
        if idx == 0:
            if a == Z:
                return self.swap_outputs(a, m)
            else:
                return
        if m == Z:
            for (f_, m_, c_), v in self.gates_.items():
                if f_ == "XOR" and (v == m_ or v == c_):
                    b = self.gates_[Gate("AND", m_, c_)]
                    if Gate("OR", a, b) in self.gates_:
                        return self.swap_outputs(v, Z)
        if a == Z:
            for (f_, m_, c_), v in self.gates_.items():
                if f_ == "XOR" and (m_ == m or c_ == m):
                    return self.swap_outputs(v, Z)
        # m ^ c = z
        f, m_, c_ = self.gates[Z]
        if f == "XOR" and m != m_ and m != c_:
            return self.swap_outputs(a, m)
        if f == "AND":
            return self.swap_outputs(self.gates_[Gate("XOR", m_, c_)], Z)
        if f == "OR":
            for (f_, m_, c_), v in self.gates_.items():
                if f_ == "XOR" and (m_ == m or c_ == m):
                    return self.swap_outputs(v, Z)
        # m & c = b
        b = self.gates_[Gate("AND", m_, c_)]
        if (c := self.gates_.get(Gate("OR", a, b))) is None:
            for (f_, a_, b_), v in self.gates_.items():
                if f_ == "OR" and (a_ == a or b_ == a):
                    return self.swap_outputs(v, b)
        if idx == self.bits - 1:
            if c != (z := f"z{(idx + 1):02d}"):
                return self.swap_outputs(c, z)

    @aoc_timer
    def debug(self) -> str:
        _ = [self.debug_adder(idx) for idx in range(self.bits)]
        assert self.aligned()
        return ",".join(sorted(self.errors))


def main() -> None:
    print("AoC 2024\nDay 24")
    system = System(path="input.txt")
    print("Part 1:", system.add())
    print("Part 2:", system.debug())


if __name__ == "__main__":
    main()
