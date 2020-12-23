#! /usr/bin/env python
import re

class MathHomework(object):
    def __init__(self, input_filename, precedence="equal"):
        if precedence == "equal":
            self.precedence = {"+": 0, "*": 0}
        elif precedence == "addition":
            # addition is higher precedence than multiplication
            self.precedence = {"+": 1, "*": 0}

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

    def parse_expression(self, expression):
        """
        parse untokenized expression into tokenized RPN expression (list) that
        can be evaluated

        (shunting-yard algorithm)
        """
        output = []
        operators = []
        tokenized = self.tokenize(expression)
        for token in tokenized:
            if re.match("^\d+$", token):
                output.append(token)
            elif re.match("^[+*]", token):
                while (operators
                        and operators[-1] != "("
                        and self.precedence[operators[-1]] >= self.precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif re.match("^\($", token):
                operators.append(token)
            elif re.match("^\)$", token):
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                if operators and operators[-1] == "(":
                    operators.pop()
        # put everything remaining in operator queue into output
        while operators:
            output.append(operators.pop())
        return output

    def evaluate_expression(self, expression):
        rpn = self.parse_expression(expression)
        stack = []
        for token in rpn:
            if re.match("^\d+$", token):
                stack.append(int(token))
            elif re.match("^\+$", token):
                stack.append(stack.pop() + stack.pop())
            elif re.match("^\*$", token):
                stack.append(stack.pop() * stack.pop())
        return stack.pop()

if __name__ == "__main__":
    h = MathHomework("inputs/day18_test.txt")
    print(f"day18 test: {h.do_homework()}")
    h = MathHomework("inputs/day18.txt")
    print(f"day18 part1: {h.do_homework()}")
    h = MathHomework("inputs/day18.txt", precedence="addition")
    print(f"day18 part2: {h.do_homework()}")
