#! /usr/bin/env python
import re

class Messages(object):
    def _parse_rule(self, rule_num):
        rule = self.rules[rule_num]
        parsed_rule = ""
        prefix = ""
        suffix = ""
        for r in rule.split():
            if re.match("\d+", r):
                # numbers get replaced by the corresponding rule
                parsed_rule += self._parse_rule(int(r))
            elif re.match("\"[a-z]\"", r):
                # quoted letters get replaced by the letter
                parsed_rule += r.replace("\"", "")
            elif re.match("\|", r):
                # pipes don't get replaced, but characters on either side get grouped
                parsed_rule += "|"
                prefix = "("
                suffix = ")"
            else:
                parsed_rule += r

        parsed_rule = prefix + parsed_rule + suffix
        return parsed_rule

    def __init__(self, input_filename, part2=False):
        self.rules = {}
        self.messages = []

        with open(input_filename, "r") as infile:
            for line in infile:
                match = re.match("(\d+): (.*)$", line)
                if match:
                    self.rules[int(match.group(1))] = match.group(2)
                elif line.strip():
                    self.messages.append(line.strip())

        if part2:
            # rule 8 becomes "42 | 42 8" (i.e. 42+)
            self.rules[8] = "42 +" # will be parsed to 42+
            # rule 11 becomes "42 31 | 41 11 31" (i.e. 42 31, or 42 42 31 31, or 42 42 42 31 31 31, or ...)
            # we'll write the regex as: (42{1} 31{1} | 42{2} 31{2} | ... | 42{40} 31{40})
            rule11 = ["("]
            for n in range(1, 40): # limit recursion depth to 40
                rule11.append(f"42 {{{n}}}")
                rule11.append(f"31 {{{n}}}")
                rule11.append("|")
            rule11[-1] = ")"
            self.rules[11] = " ".join(rule11)

        for rule_num in self.rules:
            self.rules[rule_num] = self._parse_rule(rule_num)

    def check_message(self, message):
        return bool(re.match("^" + self.rules[0] + "$", message))

    def count_matching_messages(self):
        matches = [self.check_message(message) for message in self.messages]
        print(matches)
        return [self.check_message(message) for message in self.messages].count(True)

if __name__ == "__main__":
    # m = Messages("inputs/day19_test.txt")
    m = Messages("inputs/day19_test2.txt")
    print(f"day19 test2: {m.count_matching_messages()}")
    m = Messages("inputs/day19.txt")
    print(f"day19 part1: {m.count_matching_messages()}")
    m = Messages("inputs/day19_test3.txt", part2=True)
    print(f"day19 part2 test: {m.count_matching_messages()}")
    m = Messages("inputs/day19.txt", part2=True)
    print(f"day19 part2: {m.count_matching_messages()}")
