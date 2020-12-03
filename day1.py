#! /usr/bin/env python
import itertools
import functools

class ExpenseReport(object):
    """ Class to represent an expense report (list of expenses) """
    def __init__(self, input_filename):
        """ Initialize an expense report from an input list of expenses """
        with open(input_filename, "r") as infile:
            self.input_list = [int(line) for line in infile]

    def find_values_that_sum(self, goal, num_values):
        """ Find the combination of values (num_values long) that sums to goal """
        for comb in itertools.combinations(self.input_list, num_values):
            if sum(comb) == goal:
                return comb
        return None

    def find_answer(self, num_values):
        """ Find the product of the combination of num_values values that sums to goal """
        values = self.find_values_that_sum(2020, num_values)
        return functools.reduce(lambda a, b : a*b, values)


if __name__ == "__main__":
    e = ExpenseReport("inputs/day1_test.txt")
    print("Part 1a test: {}".format(e.find_answer(2)))
    e = ExpenseReport("inputs/day1.txt")
    print("Part 1a: {}".format(e.find_answer(2)))
    print("Part 1b: {}".format(e.find_answer(3)))
