#! /usr/bin/env python
import functools

class BagRules(object):
    def __init__(self, input_filename):
        self.rules = {}
        with open(input_filename, "r") as infile:
            for line in infile:
                rule = {}
                outer_color = line.split()[0] + " " + line.split()[1]
                contents = line.split(" contain ")[1]
                for c in contents.split(", "):
                    if "no other bags." not in c:
                        quantity = int(c.split()[0])
                        inner_color = c.split()[1] + " " + c.split()[2]
                        rule[inner_color] = quantity
                self.rules[outer_color] = rule

    def can_bag_contain(self, outer_color, inner_color):
        """ return true iff outer_color can contain inner_color """
        if not self.rules[outer_color]:
            # can't contain any bags
            return False
        elif inner_color in self.rules[outer_color].keys():
            # outer_color directly contains inner_color
            return True
        else:
            # search inner bags
            results = [self.can_bag_contain(o, inner_color) for o in self.rules[outer_color].keys()]
            return functools.reduce(lambda a, b: a or b, results)

    def count_bags_containing(self, inner_color="shiny gold"):
        """ count the number of bags that contain at least one inner_color bag """
        return sum([self.can_bag_contain(outer_color, inner_color)
            for outer_color in self.rules.keys()])

    def count_how_many_bags_within(self, outer_color):
        """ count the total number of bags inside of an outer_color bag, including the outer bag """
        total = 1 # count itself
        bags_to_search = self.rules[outer_color]
        for color in bags_to_search.keys():
            total += bags_to_search[color] * self.count_how_many_bags_within(color)
        return total


if __name__ == "__main__":
    b = BagRules("inputs/day7a_test.txt")
    print(f"day7a test: {b.count_bags_containing('shiny gold')}")
    b = BagRules("inputs/day7.txt")
    print(f"day7a: {b.count_bags_containing('shiny gold')}")
    b = BagRules("inputs/day7b_test.txt")
    print(f"day7b test: {b.count_how_many_bags_within('shiny gold') - 1}")
    b = BagRules("inputs/day7.txt")
    print(f"day7b: {b.count_how_many_bags_within('shiny gold') - 1}")

