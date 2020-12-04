#! /usr/bin/env python

class PasswordPolicy(object):
    """ Class to represent a password policy (character and two integers)"""
    def __init__(self, policy_string):
        s = policy_string.split(" ")
        minmax = s[0].split("-")
        self.a = int(minmax[0])
        self.b = int(minmax[1])
        self.char = s[1]

    def check_password(self, password, policy="sled"):
        """
        Return true iff password meets specified policy.
        sled: password must have between a and b occurences of char, inclusive.
        toboggan: either password[a-1] or password[b-1] must be char, but not both.
        """

        if policy == "sled":
            return (self.a <= password.count(self.char) <= self.b)
        elif policy == "toboggan":
            return (password[self.a - 1] == self.char) ^ (password[self.b - 1] == self.char)
        else:
            raise Exception("policy must be 'sled' or 'toboggan'")


class PasswordDatabase(object):
    """ Class to represent a password database.

    A password database is a list of passwords and the password policy for when
    each password was created.
    """
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            self.database = [(PasswordPolicy(line.split(":")[0]),
                              line.split(":")[1].strip()) for line in infile]

    def count_valid_passwords(self, policy="sled"):
        return [p[0].check_password(p[1], policy) for p in self.database].count(True)

if __name__ == "__main__":
    p = PasswordDatabase("inputs/day2_test.txt")
    print("Day 2 test: {}".format(p.count_valid_passwords()))
    p = PasswordDatabase("inputs/day2.txt")
    print("Day 2a: {}".format(p.count_valid_passwords()))
    p = PasswordDatabase("inputs/day2.txt")
    print("Day 2b: {}".format(p.count_valid_passwords(policy="toboggan")))

