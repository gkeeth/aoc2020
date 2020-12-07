#! /usr/bin/env python

class CustomsGroup(object):
    """ class to represent a group travelling together """
    def __init__(self, forms):
        """
        construct a CustomsGroup from a list of forms (list of strings where
        each character is a question for which the answer is yes)

        """
        self.num_travellers = len(forms)
        self.forms = forms
        # flattened = [c for form in forms for c in form]
        # form_set = set(flattened)
        # if and_or == "OR":
        #     self.yes_answers = list(form_set)
        # elif and_or == "AND":
        #     self.yes_answers = [c for c in form_set if flattened.count(c) == len(forms)]

    def count_yes_answers(self, and_or="OR"):
        """
        count questions the group has answered "yes" to

        if and_or is "OR", the group is considered to have answered "yes" to a
        question if anyone answers "yes"
        if and_or is "AND", the group is considered to have answered "yes" to a
        question only if everyone answers "yes"
        """
        flattened = [c for form in self.forms for c in form]
        if and_or == "OR":
            return len(set(flattened))
        elif and_or == "AND":
            return len([c for c in set(flattened) if flattened.count(c) == self.num_travellers])




class Plane(object):
    """ class to represent an entire plane's worth of groups of travellers """
    def __init__(self, input_filename):
        self.groups = []
        with open(input_filename, "r") as infile:
            group = []
            for line in infile:
                if line.strip() == "":
                    self.groups.append(CustomsGroup(group))
                    group = []
                else:
                    group.append(line.strip())
            self.groups.append(CustomsGroup(group))

    def sum_yes_answers(self, and_or="OR"):
        """
        sum counts of questions each group has answered "yes" to

        if and_or is "OR", the group is considered to have answered "yes" to a
        question if anyone answers "yes"
        if and_or is "AND", the group is considered to have answered "yes" to a
        question only if everyone answers "yes"
        """
        return sum([g.count_yes_answers(and_or) for g in self.groups])

if __name__ == "__main__":
    p = Plane("inputs/day6_test.txt")
    print(f"day6 test: {p.sum_yes_answers()}")
    p = Plane("inputs/day6.txt")
    print(f"day6a: {p.sum_yes_answers()}")
    print(f"day6b: {p.sum_yes_answers(and_or='AND')}")
