# %% Day 17
from helper import aoc_timer
from collections import deque
from copy import deepcopy
import re

type Data = list[str]


class Computer:
    def __init__(self, path: str) -> None:
        self.ip = 0
        self.R = {}
        self.P = []
        self.output = []
        self.get_input(path)

    @aoc_timer
    def get_input(self, path: str) -> None:
        with open(path) as f:
            registers, program = f.read().split("\n\n")
        for r, n in re.findall(r"Register (\w+): (\d+)", registers):
            self.R[r] = int(n)
        _, program = program.split(": ")
        for idx, n in enumerate(program.split(",")):
            self.P.append(int(n))
        self.max_ip = idx
        self.R_ = self.R.copy()

    def reset(self) -> None:
        self.ip = 0
        self.R = self.R_.copy()
        self.output = []

    def combo(self, operand: int) -> int:
        return {
            4: self.R["A"],
            5: self.R["B"],
            6: self.R["C"],
            7: None,
        }.get(operand, operand)

    def out(self) -> str:
        return ",".join(map(str, self.output))

    def replicated(self, partial: bool = True) -> bool:
        if partial:
            return self.output == self.P[-len(self.output):]
        return self.output == self.P

    def run(self) -> None:
        while self.ip < self.max_ip:
            opcode, operand = self.P[self.ip], self.P[self.ip + 1]
            self.ip += 2
            match opcode:
                case 0:
                    self.R["A"] >>= self.combo(operand)
                case 1:
                    self.R["B"] ^= operand
                case 2:
                    self.R["B"] = self.combo(operand) % 8
                case 3:
                    if self.R["A"]:
                        self.ip = operand
                case 4:
                    self.R["B"] ^= self.R["C"]
                case 5:
                    self.output.append(self.combo(operand) % 8)
                case 6:
                    self.R["B"] = self.R["A"] >> self.combo(operand)
                case 7:
                    self.R["C"] = self.R["A"] >> self.combo(operand)
                case _:
                    assert False, opcode

        @staticmethod
        def run_deconstructed(a: int) -> list[int]:
            """
            Deconstructed input program for the purposes of solving the puzzle. Used to
            test various starting values for the A register versus the program output.
            The A register is processed in octal and the B and C registers are used as
            temporary storage for intermediate calculations.
            """
            out = []
            while True:
                b = a % 8 ^ 6
                c = a >> b
                b ^= c ^ 4
                out.append(b % 8)
                a >>= 3
                if a == 0:
                    return out


@aoc_timer
def solve(vm: Computer) -> tuple[str, int]:
    vm.run()
    p1 = vm.out()
    Q = deque([(idx := -1, 0, deepcopy(vm))])
    while Q and idx <= vm.max_ip:
        idx, a, vm = Q.popleft()
        if vm.replicated(partial=False):
            return p1, a
        idx += 1
        a *= 8
        for offset in range(8):
            vm.reset()
            vm.R["A"] = a + offset
            vm.run()
            if vm.replicated(partial=True):
                Q.append((idx, a + offset, deepcopy(vm)))
    return p1, None


def main() -> None:
    print("AoC 2024\nDay 17")
    vm = Computer("input.txt")
    p1, p2 = solve(vm)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
