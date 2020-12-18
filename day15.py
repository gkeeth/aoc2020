#! /usr/bin/env python
import collections

class MemoryGame(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            line = infile.readlines()[0].strip()
            self.starting_length = len(line.split(","))
            # number: (round last said, number of times said)
            self.numbers = {int(num): (index, 0) for index, num in enumerate(line.split(","))} # ordered since 3.7
            self.round = 0

    def play_round(self):
        if self.round < self.starting_length:
            self.last_num = list(self.numbers.keys())[self.round]
            self.numbers[self.last_num] = (self.round, self.numbers[self.last_num][1] + 1)
            print(f"round {self.round}: {self.last_num} (starting)")
        else:
            if self.numbers[self.last_num][1] == 1:
                # number from last round was spoken for the first time
                self.numbers[0] = (self.numbers[0][0], self.numbers[0][1] + 1)
                self.last_num = 0
                print(f"round {self.round}: 0 (last number new)")
            else:
                age = self.round - 1 - self.numbers[self.last_num][0]
                print(f"round: {self.round}, age: {age}")
                self.numbers[age] = (self.round, self.numbers[age][1] + 1)
                last_times = self.numbers[self.last_num][1]
                self.last_num = age
                print(f"round {self.round}: {age} (last number repeat, spoken {last_times} times)")
        self.round += 1
        return self.last_num

    def play(self, rounds=2020):
        for n in range(rounds):
            num = self.play_round()
        return num


if __name__ == "__main__":
    g = MemoryGame("inputs/day15_test1.txt")
    print(f"day15 test1: {g.play(rounds=10)}")
