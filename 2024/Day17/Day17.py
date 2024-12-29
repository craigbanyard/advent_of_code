# %% Day 17
from helper import aoc_timer
from collections import deque
from copy import deepcopy
import re


class Computer:
    def __init__(self, path: str, disassembled: bool = False) -> None:
        self.ip = 0
        self.R = {}
        self.P = []
        self.output = []
        self.disassembled = disassembled
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
        return [0, 1, 2, 3, self.R["A"], self.R["B"], self.R["C"]][operand]

    def out(self) -> str:
        return ",".join(map(str, self.output))

    def replicated(self, partial: bool = True) -> bool:
        if partial:
            return self.output == self.P[-len(self.output):]
        return self.output == self.P

    def run(self) -> None:
        if self.disassembled:
            return self.run_disassembled()
        while self.ip < self.max_ip:
            opcode, operand = self.P[self.ip : self.ip + 2]
            self.ip += 2
            match opcode:
                case 0:
                    self.R["A"] >>= self.combo(operand)
                case 1:
                    self.R["B"] ^= operand
                case 2:
                    self.R["B"] = self.combo(operand) & 7
                case 3:
                    if self.R["A"]:
                        self.ip = operand
                case 4:
                    self.R["B"] ^= self.R["C"]
                case 5:
                    self.output.append(self.combo(operand) & 7)
                case 6:
                    self.R["B"] = self.R["A"] >> self.combo(operand)
                case 7:
                    self.R["C"] = self.R["A"] >> self.combo(operand)
                case _:
                    assert False, opcode

    def run_disassembled(self) -> None:
        """
        Disassembled input program for the purposes of solving the puzzle. Used to test
        various starting values for the A register versus the program output. The A
        register is processed in octal, consuming its least significant three bits on
        each iteration, whilst the B and C registers are used as temporary storage for
        intermediate calculations.
        To solve, we work backwards through the input program, determining which input
        values for the A register yield the desired digit of the program. We continue in
        a BFS-like walk, adding three bits (multiplying by 8) and varying those new bits
        (adding offsets between 0 and 7) until we match all digits of the input program.
        """
        a = self.R["A"]
        while True:
            b = a & 7 ^ 6
            c = a >> b
            b ^= c ^ 4
            self.output.append(b & 7)
            a >>= 3
            if a == 0:
                return


@aoc_timer
def solve(vm: Computer) -> tuple[str, int]:
    vm.run()
    p1 = vm.out()
    vm.reset()
    Q = deque([(-1, 0, deepcopy(vm))])
    while Q:
        idx, a, vm = Q.popleft()
        if vm.replicated(partial=False):
            return p1, a
        if idx > vm.max_ip:
            continue
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
    vm = Computer("input.txt", disassembled=False)
    p1, p2 = solve(vm)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
