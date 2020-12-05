#! /usr/bin/env python
import re

class Passport(object):
    """ Class to represent a Passport """

    def __init__(self, batch_lines):
        self.fields = {}
        for line in batch_lines:
            for field in line.split():
                self.fields[field.split(":")[0]] = field.split(":")[1]

    def _check_birth_year(self):
        return ("byr" in self.fields.keys()
                and 1920 <= int(self.fields["byr"]) <= 2002)
    def _check_issue_year(self):
        return ("iyr" in self.fields.keys()
                and 2010 <= int(self.fields["iyr"]) <= 2020)
    def _check_expiration_year(self):
        return ("eyr" in self.fields.keys()
                and 2020 <= int(self.fields["eyr"]) <= 2030)
    def _check_height(self):
        try:
            unit = self.fields["hgt"][-2:]
            value = int(self.fields["hgt"][:-2])
            return ((unit == "cm" and 150 <= value <= 193)
                    or (unit == "in" and 59 <= value <= 76))
        except:
            # "hgt" field is not present, or field is malformed
            return False
    def _check_hair_color(self):
        regex = "^#[a-z0-9]{6}$"
        return ("hcl" in self.fields.keys()
                and re.search(regex, self.fields["hcl"]) is not None)
    def _check_eye_color(self):
        return ("ecl" in self.fields.keys()
                and self.fields["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    def _check_passport_id(self):
        regex = "^[0-9]{9}$"
        return ("pid" in self.fields.keys()
                and re.search(regex, self.fields["pid"]) is not None)
    def _check_country_id(self):
        return True

    def check_validity(self, advanced=False):
        """
        Check validity of passport.

        If advanced is true, validates contents of each field.
        Otherwise, checks if mandatory fields are present (all except "cid")
        """
        if advanced:
            return (self._check_birth_year()
                    and self._check_issue_year()
                    and self._check_expiration_year()
                    and self._check_height()
                    and self._check_hair_color()
                    and self._check_eye_color()
                    and self._check_passport_id()
                    and self._check_country_id())
        else:
            return (len(self.fields.keys()) == 8
                    or (len(self.fields.keys()) == 7 and "cid" not in self.fields.keys()))

class PassportBatch(object):
    """ Class to represent passport batch file """
    def __init__(self, input_filename):
        self.passports = []
        with open(input_filename, "r") as infile:
            passport_lines = []
            for line in infile:
                if line.strip() == "":
                    if passport_lines:
                        self.passports.append(Passport(passport_lines))
                    passport_lines = []
                else:
                    passport_lines.append(line)
            # last passport isn't followed by an empty line
            if passport_lines:
                self.passports.append(Passport(passport_lines))

    def count_valid_passports(self, advanced=False):
        """
        Count the number of valid passports in the batch file.

        If advanced == True, use comprehensive set of checks; otherwise just
        check that mandatory fields are present (all except "cid")
        """

        return [p.check_validity(advanced) for p in self.passports].count(True)


if __name__ == "__main__":
    b = PassportBatch("inputs/day4_test.txt")
    print("day 4 test: {}".format(b.count_valid_passports()))
    b = PassportBatch("inputs/day4.txt")
    print("day 4a: {}".format(b.count_valid_passports()))
    print("day 4b: {}".format(b.count_valid_passports(advanced=True)))
