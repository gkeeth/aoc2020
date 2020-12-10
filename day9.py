#! /usr/bin/env python
import itertools

class XMASData(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            self.data = [int(line) for line in infile]

    def find_first_invalid_number(self, preamble_length=25):
        """
        return first number that fails data validity check

        a number is valid if it is the sum of any two of the previous 25 numbers
        """
        for n in range(preamble_length, len(self.data)):
            solution_found = False
            # check if self.data[n] is sum of any two values in past 25
            for i, j in itertools.combinations(range(n - preamble_length, n), 2):
                    if self.data[i] + self.data[j] == self.data[n]:
                        solution_found = True
                        break
            if not solution_found:
                return self.data[n]

    def find_encryption_weakness(self, preamble_length=25):
        """
        return sum of smallest and largest numbers in first sequence that sums
        to the first invalid number
        """
        first_invalid_number = self.find_first_invalid_number(preamble_length)
        for n in range(len(self.data)):
            total = self.data[n]
            smallest = self.data[n]
            largest = self.data[n]
            j = n + 1
            while total < first_invalid_number and j < len(self.data):
                total += self.data[j]
                smallest = min(smallest, self.data[j])
                largest = max(largest, self.data[j])
                j += 1
            if total == first_invalid_number:
                return smallest + largest


if __name__ == "__main__":
    x = XMASData("inputs/day9_test.txt")
    print(f"day9a test: {x.find_first_invalid_number(preamble_length=5)}")
    print(f"day9b test: {x.find_encryption_weakness(preamble_length=5)}")
    x = XMASData("inputs/day9.txt")
    print(f"day9a: {x.find_first_invalid_number()}")
    print(f"day9a: {x.find_encryption_weakness()}")


