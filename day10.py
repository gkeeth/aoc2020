#! /usr/bin/env python
import itertools
import collections

class AdapterCollection(object):
    """ class to represent a collection of Joltage Adapters """
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            adapters = sorted([int(line) for line in infile])
            self.highest = adapters[-1]
            # include seatback output (0) and device itself (highest + 3)
            self.adapters = [0] + adapters + [self.highest + 3]

    def get_all_deltas(self):
        """ return list of deltas from one adapter to the next """
        return [b - a for a, b in zip(self.adapters, self.adapters[1:])]

    def get_distribution(self):
        """ return number of 1-deltas times number of 3-deltas """
        counted = collections.Counter(self.get_all_deltas())
        return counted[1] * counted[3]

    def count_options_naive(self, starting_value=0):
        """
        count the combinations of adapters using recursion, from 0 Jolts
        (seatback) to device. Correct but too slow for full input.
        """
        options = 0
        if starting_value + 1 in self.adapters:
            options += self.count_options_naive(starting_value + 1)
        if starting_value + 2 in self.adapters:
            options += self.count_options_naive(starting_value + 2)
        if starting_value + 3 in self.adapters:
            options += self.count_options_naive(starting_value + 3)
        if starting_value == self.highest:
            options = 1
        return options

    def count_options_memo(self):
        self.memo = {}
        return self._count_options_memo(self.highest+3)

    def _count_options_memo(self, start):
        try:
            return self.memo[start]
        except:
            options = 0
            if start - 1 in self.adapters:
                options += self._count_options_memo(start - 1)
            if start - 2 in self.adapters:
                options += self._count_options_memo(start - 2)
            if start - 3 in self.adapters:
                options += self._count_options_memo(start - 3)
            if start == 0:
                options = 1
            self.memo[start] = options
            return options

    def count_options_math(self):
        """
        count the combinations of adapters using some math. Does not allow for
        Joltage differences of 2 jolts, just 1 or 3. This is true by inspection
        of input data, but not guaranteed by problem statement.
        """

        deltas = self.get_all_deltas()
        prev = deltas[0]
        count = 0
        runs = []
        for d in deltas:
            if d != prev:
                runs.append((prev, count))
                prev = d
                count = 1
            else:
                count += 1
        runs.append((prev, count))
        combinations = 1
        for r in runs:
            # for each run of 1 jolt deltas, multiply combinations by a factor
            # related to run length (tribonacci sequence)
            factors = {
                    1: 1,
                    2: 2,
                    3: 4,
                    4: 7,
                    5: 13,
                    # ...don't expect any runs longer than 5
                    }
            # tribonacci sequence...
            if r[0] == 1:
                combinations *= factors[r[1]]
            elif r[0] == 2:
                raise Exception("wasn't expecting a joltage difference of 2")
        return combinations


if __name__ == "__main__":
    a = AdapterCollection("inputs/day10_test1.txt")
    print(f"day10 test1a: {a.get_distribution()}")
    print(f"day10 test1b naive: {a.count_options_naive()}")
    print(f"day10 test1b math: {a.count_options_math()}")
    print(f"day10 test1b memo: {a.count_options_memo()}")
    a = AdapterCollection("inputs/day10_test2.txt")
    print(f"day10 test2a: {a.get_distribution()}")
    print(f"day10 test2b naive: {a.count_options_naive()}")
    print(f"day10 test2b math: {a.count_options_math()}")
    print(f"day10 test2b memo: {a.count_options_memo()}")
    a = AdapterCollection("inputs/day10.txt")
    print(f"day10 part1: {a.get_distribution()}")
    print(f"day10 part2 math: {a.count_options_math()}")
    print(f"day10 part2 memo: {a.count_options_memo()}")
