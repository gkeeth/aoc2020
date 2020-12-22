#! /usr/bin/env python
import re

class MathHomework(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            self.expressions = [line.strip() for line in infile]

    @staticmethod
    def tokenize(expression):
        tokenized = []
        token = ""
        for c in expression:
            if c == " ":
                if token != "":
                    tokenized.append(token)
                    token = ""
            elif c == "*" or c == "+":
                token = c # token will be terminated & appended to list by following " "
            elif c == "(":
                # previous character has always been tokenized already
                token = c
                tokenized.append(token)
                token = ""
            elif c == ")":
                # previous character could be a digit, space, or ")"
                # digit: previous token is unterminated
                # space: previous token is terminated
                # ")": previous token is terminated
                if token != "":
                    tokenized.append(token)
                token = c
                tokenized.append(token)
                token = ""
            else:
                # digit. Token will be terminated and appended by " ", ")", or end of expression
                token += c
        # if last token is a digit, it needs to be added manually
        if token != "":
            tokenized.append(token)
        return tokenized

    def do_homework(self):
        """ return sum of all expression in homework """
        return sum([self.evaluate_expression(expression)
            for expression in self.expressions])

    def evaluate_expression(self, expression):
        tokenized = self.tokenize(expression)
        # print(tokenized)
        a = 0
        op = ""
        stored = []
        for token in tokenized:
            if re.match("^\d+$", token):
                if op == "":
                    a = int(token)
                elif op == "*":
                    a *= int(token)
                    op = ""
                    # print(a)
                elif op == "+":
                    a += int(token)
                    op = ""
                    # print(a)
            elif re.match("^[+*]$", token):
                op = token
            elif re.match("^\($", token):
                stored.append((a, op))
                a = 0
                op = ""
            elif re.match("^\)$", token):
                temp = stored.pop()
                if temp[1] == "*":
                    a = temp[0] * a
                    op = ""
                    # print(a)
                elif temp[1] == "+":
                    a = temp[0] + a
                    op = ""
                    # print(a)
                elif temp[1] == "":
                    op = ""
        print(f"total: {a}")
        return a

if __name__ == "__main__":
    h = MathHomework("inputs/day18_test.txt")
    print(f"day18 test: {h.do_homework()}")
    h = MathHomework("inputs/day18.txt")
    print(f"day18 part1: {h.do_homework()}")
