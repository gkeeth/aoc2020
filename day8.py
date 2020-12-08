#! /usr/bin/env python
import copy

class Instruction(object):
    """
    Class to represent a single instruction (opcode and arg).
    Instructions also store whether or not they have been previously executed.
    """
    def __init__(self, instruction):
        self.op = instruction.split()[0].strip()
        self.arg = int(instruction.split()[1].strip())
        self.executed = False

    def run(self, state):
        self.executed = True

        if self.op == "nop":
            state.pc += 1
        elif self.op == "acc":
            state.pc += 1
            state.acc += self.arg
        elif self.op == "jmp":
            state.pc += self.arg

class Computer(object):
    """
    Class to represent the state of a computer (registers and program)
    """
    def __init__(self, input_filename):
        self.program = []
        self.pc = 0
        self.acc = 0

        with open(input_filename, "r") as infile:
            self.program = [Instruction(line) for line in infile]

    def run(self):
        """
        Run program until any instruction would be repeated.
        When an instruction is about to be repeated, instead return the value
        in acc.
        """
        while not self.program[self.pc].executed and self.pc < len(self.program):
            self.program[self.pc].run(self)
        return self.acc

    def find_corrupted_instruction(self):
        for pc in range(len(self.program)):
            comp = copy.deepcopy(self)
            # swap "jmp" and "nop"
            if comp.program[pc].op == "nop":
                comp.program[pc].op = "jmp"
            elif comp.program[pc].op == "jmp":
                comp.program[pc].op = "nop"
            else:
                # nothing swapped; move on to next instruction
                continue

            # run modified program
            while not comp.program[comp.pc].executed:
                comp.program[comp.pc].run(comp)
                if comp.pc >= len(comp.program):
                    # found our instruction
                    return pc, comp.acc
        print("solution not found")


if __name__ == "__main__":
    c = Computer("inputs/day8_test.txt")
    print(f"day8 test: {c.run()}")
    c = Computer("inputs/day8.txt")
    print(f"day8a: {c.run()}")
    c = Computer("inputs/day8_test.txt")
    print(f"day8 test: {c.find_corrupted_instruction()[1]}")
    c = Computer("inputs/day8.txt")
    print(f"day8b: {c.find_corrupted_instruction()[1]}")
