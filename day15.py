#! /usr/bin/env python
import collections

class MemoryGame(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            line = infile.readlines()[0].strip()
            self.starting_length = len(line.split(","))
            # number: tuple of last two rounds in which it was said
            self.numbers = {int(num): [] for num in line.split(",")} # ordered since 3.7
            self.numbers = {int(num): () for num in line.split(",")} # ordered since 3.7
            self.round = 0

    def play_round(self):
        if self.round < self.starting_length:
            self.last_num = list(self.numbers.keys())[self.round]
            if self.numbers[self.last_num]:
                self.numbers[self.last_num] = (self.numbers[self.last_num][-1], self.round)
            else:
                self.numbers[self.last_num] = (self.round,)
        else:
            if len(self.numbers[self.last_num]) == 1:
                # number from last round was spoken for the first time
                try:
                    self.numbers[0] = (self.numbers[0][-1], self.round)
                except:
                    self.numbers[0] = (self.round,)

                self.last_num = 0
            else:
                age = self.numbers[self.last_num][-1] - self.numbers[self.last_num][-2]
                try:
                    self.numbers[age] = (self.numbers[age][-1], self.round)
                except:
                    self.numbers[age] = (self.round,)
                self.last_num = age
        self.round += 1
        return self.last_num

    def play(self, rounds=2020):
        for n in range(rounds):
            num = self.play_round()
        return num


if __name__ == "__main__":
    g = MemoryGame("inputs/day15_test1.txt")
    print(f"day15 test1: {g.play(rounds=10)}")
    g = MemoryGame("inputs/day15_test1.txt")
    print(f"day15 test1: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test2.txt")
    print(f"day15 test2: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test3.txt")
    print(f"day15 test3: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test4.txt")
    print(f"day15 test4: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test5.txt")
    print(f"day15 test5: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test6.txt")
    print(f"day15 test6: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test7.txt")
    print(f"day15 test7: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15.txt")
    print(f"day15 part1: {g.play(rounds=2020)}")
    g = MemoryGame("inputs/day15_test1.txt")
    print(f"day15 test1: {g.play(rounds=30000000)}")
    g = MemoryGame("inputs/day15.txt")
    print(f"day15 part2: {g.play(rounds=30000000)}")
