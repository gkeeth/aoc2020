#! /usr/bin/env python
import re

class FerryProgram(object):
    def __init__(self, input_filename):
        self.pc = 0
        self.mask = "0"
        self.memory = {}
        with open(input_filename, "r") as infile:
            self.program = [(line.split("=")[0].strip(), line.split("=")[1].strip())
                    for line in infile]

    def _generate_floating_addresses(self, addr, mask):
        """ return a list of all floating permutations of addr """
        if "X" in mask:
            i = mask.find("X")
            mask = mask.replace("X", "0", 1)
            return (self._generate_floating_addresses(addr[:i] + "0" + addr[i+1:], mask)
                    + self._generate_floating_addresses(addr[:i] + "1" + addr[i+1:], mask))
        else:
            return [int(addr, 2)]

    def execute(self, mode="data"):
        """
        execute the instruction at pc.

        if mode is "data", apply mask to data before writing it to memory.
        if mode is "addr", apply mask to address before writing data to memory.
        """
        if self.program[self.pc][0] == "mask":
            self.mask = self.program[self.pc][1]
        elif "mem" in self.program[self.pc][0]:
            addr = int(re.match("^mem\[(\d+)\]$", self.program[self.pc][0]).group(1))
            data = int(self.program[self.pc][1])
            if mode == "addr":
                mask_or = int(self.mask.replace("X", "0"), 2)
                addresses = self._generate_floating_addresses(format(addr | mask_or, "036b"), self.mask)
                for a in addresses:
                    self.memory[a] = data
            elif mode == "data":
                mask_and = int(self.mask.replace("X", "1"), 2)
                mask_or = int(self.mask.replace("X", "0"), 2)
                data = (data | mask_or) & mask_and
                self.memory[addr] = data

    def run(self, mode="data"):
        program_length = len(self.program)
        while self.pc < program_length:
            self.execute(mode)
            self.pc += 1

    def sum_values_in_memory(self, mode="data"):
        total = 0
        self.run(mode)
        for val in self.memory.values():
            total += val
        return total

if __name__ == "__main__":
    p = FerryProgram("inputs/day14_test.txt")
    print(f"day 14a test: {p.sum_values_in_memory()}")
    p = FerryProgram("inputs/day14b_test.txt")
    print(f"day 14b test: {p.sum_values_in_memory(mode='addr')}")
    p = FerryProgram("inputs/day14.txt")
    print(f"day 14a: {p.sum_values_in_memory()}")
    p = FerryProgram("inputs/day14.txt")
    print(f"day 14b: {p.sum_values_in_memory(mode='addr')}")
