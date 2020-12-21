#! /usr/bin/env python
import re
import copy

class TicketRule(object):
    def __init__(self, line):
        # by inspection of inputs, all rules are in form "a-b or x-y"
        match = re.match("^([ a-zA-Z]+): (\d+-\d+) or (\d+-\d+)$", line)
        self.name = match.groups()[0]
        self.ranges = []
        for v in match.groups()[1:]:
            self.ranges.append((int(v.split("-")[0]), int(v.split("-")[1])))

    def check_value(self, value):
        """ return true iff value is valid for rule """
        for r in self.ranges:
            if r[0] <= value <= r[1]:
                return True
        return False

class Ticket(object):
    def __init__(self, line):
        self.values = [int(v) for v in line.split(",")]

    def check_validity(self, ticket_rules):
        """ return list of values that do not match any rule """
        invalid_values = []
        for v in self.values:
            validity = [rule.check_value(v) for rule in ticket_rules]
            if not True in validity:
                invalid_values.append(v)
        return invalid_values

class TicketInformation(object):
    def __init__(self, input_filename):
        self.rules = []
        self.nearby = []
        self.field_mapping = {} # map field index to field name
        with open(input_filename, "r") as infile:
            state = "rules"
            for line in infile:
                if line.strip() == "":
                    continue

                # state transitions
                if "your ticket:" in line:
                    state = "your ticket"
                    continue
                elif "nearby tickets" in line:
                    state = "nearby tickets"
                    continue

                if state == "rules":
                    self.rules.append(TicketRule(line))
                elif state == "your ticket":
                    self.ticket = Ticket(line)
                elif state == "nearby tickets":
                    self.nearby.append(Ticket(line))
        self.num_fields = len(self.ticket.values)

    def check_nearby_tickets(self):
        """ return sum of invalid values in nearby tickets (error rate) """
        error_rate = 0
        for t in self.nearby:
            invalid_values = t.check_validity(self.rules)
            if invalid_values:
                error_rate += sum(invalid_values)
        return error_rate

    def discard_invalid_tickets(self):
        """
        check validity of all nearby tickets, and remove them if they are
        not valid.
        """
        for t in copy.copy(self.nearby):
            if t.check_validity(self.rules):
                self.nearby.remove(t)

    def map_fields(self):
        # map positions to possible rules: e.g. 0 -> [0 (class), 1 (row), (seat)]
        positions_to_possible_rules = [copy.copy(self.rules) for f in range(len(self.nearby[0].values))]
        for f in range(len(self.nearby[0].values)):
            for rule in self.rules:
                for n, t in enumerate(self.nearby):
                    if not rule.check_value(t.values[f]):
                        # rule can't match to field f
                        positions_to_possible_rules[f].remove(rule)
                        break
        repeat = True
        while repeat:
            repeat = False
            for f, rule_list in enumerate(positions_to_possible_rules):
                # eliminate rules that have already been assigned to a field
                for key in self.field_mapping:
                    if len(rule_list) > 1 and self.field_mapping[key] in rule_list:
                        rule_list.remove(self.field_mapping[key])
                        repeat = True # run again to check if any new rules can be mapped
                if len(rule_list) == 1:
                    self.field_mapping[f] = rule_list[0]
                    if not repeat: # we're done, print mappings
                        print(f"mapped field {f}: {self.field_mapping[f].name}")

        for f, possibilities in enumerate(positions_to_possible_rules):
            if len(possibilities) != 1:
                raise(Exception(f"too many possibilities remaining for field {f}: {[p.name for p in possibilities]}"))


    def get_part2_answer(self):
        self.discard_invalid_tickets()
        self.map_fields()
        product = 1
        for key in self.field_mapping:
            if re.match("^departure.*$", self.field_mapping[key].name):
                product *= self.ticket.values[key]
        return product




if __name__ == "__main__":
    t = TicketInformation("inputs/day16_test.txt")
    print(f"day16 part1 test: {t.check_nearby_tickets()}")
    t = TicketInformation("inputs/day16_test2.txt")
    t.discard_invalid_tickets()
    t.map_fields()
    t = TicketInformation("inputs/day16.txt")
    print(f"day16 part1: {t.check_nearby_tickets()}")
    t = TicketInformation("inputs/day16.txt")
    print(f"day16 part2: {t.get_part2_answer()}")

