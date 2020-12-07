#! /usr/bin/env python
class BoardingPass(object):
    """
    Class to represent a boarding pass.

    Boarding passes are defined by a seat assignment, which encodes the seat's
    row and column. The seat ID can be calculated as row * 8 + column.
    """

    def __init__(self, seatstring):
        self.seatstring = seatstring.strip()
        self.row = int(seatstring[0:7].replace("F", "0").replace("B", "1"), 2)
        self.column = int(seatstring[7:10].replace("L", "0").replace("R", "1"), 2)
        self.seat_id = self.row * 8 + self.column

    def __str__(self):
        return f"{self.seatstring}: row {self.row}, column {self.column}, seat ID {self.seat_id}"


class BoardingPassList(object):
    """ Class to represent list of boarding passes, defined by a list of seat assignments """
    def __init__(self, input_filename):
        """ construct list of boarding passes from input file of seat assignments """
        self.boarding_passes = []
        with open(input_filename, "r") as infile:
            for line in infile:
                self.boarding_passes.append(BoardingPass(line))

    def get_highest_seat_id(self):
        """ get highest seat id in list of boarding passes """
        return max([bp.seat_id for bp in self.boarding_passes])

    def get_seat_id(self):
        """ determine the seat id of your seat """
        # loop through seats; return first missing seat_id where seat_id - 1 and seat_id + 1 are both present
        seat_ids = sorted([bp.seat_id for bp in self.boarding_passes])
        for s in range(127 * 8 + 7 + 1):
            if s not in seat_ids and s-1 in seat_ids and s+1 in seat_ids:
                return s


    def print_boarding_passes(self):
        """ print details for all boarding passes in list """
        for bp in self.boarding_passes:
            print(bp)

if __name__ == "__main__":
    b = BoardingPassList("inputs/day5_test.txt")
    print("Day 5 test: {}".format(b.get_highest_seat_id()))
    b.print_boarding_passes()
    b = BoardingPassList("inputs/day5.txt")
    print("Day 5a: {}".format(b.get_highest_seat_id()))
    print("Day 5b: {}".format(b.get_seat_id()))

