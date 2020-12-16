#! /usr/bin/env python
from copy import copy

class WaitingArea(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            self.seats = [line.strip() for line in infile]

    def _get_adjacent_seats(self, row, col):
        """ return list of values of 8 adjacent seats """
        adj = []
        left = bool(col - 1 >= 0)
        right = bool(col + 1 < len(self.seats[0]))
        top = bool(row - 1 >= 0)
        bottom = bool(row + 1 < len(self.seats))
        if top:
            adj.append(self.seats[row-1][col])
            if left:
                adj.append(self.seats[row-1][col-1])
            if right:
                adj.append(self.seats[row-1][col+1])
        if bottom:
            adj.append(self.seats[row+1][col])
            if left:
                adj.append(self.seats[row+1][col-1])
            if right:
                adj.append(self.seats[row+1][col+1])
        if left:
            adj.append(self.seats[row][col-1])
        if right:
            adj.append(self.seats[row][col+1])
        return adj

    def _get_nearest_seats(self, row, col):
        def _is_seat(c):
            return bool(c in "L#")
        adj = []
        # up
        for r in range(row - 1, -1, -1):
            if _is_seat(self.seats[r][col]):
                adj.append(self.seats[r][col])
                break
        # down
        for r in range(row + 1, len(self.seats)):
            if _is_seat(self.seats[r][col]):
                adj.append(self.seats[r][col])
                break
        # right
        for c in range(col + 1, len(self.seats[0])):
            if _is_seat(self.seats[row][c]):
                adj.append(self.seats[row][c])
                break
        # left
        for c in range(col - 1, -1, -1):
            if _is_seat(self.seats[row][c]):
                adj.append(self.seats[row][c])
                break

        # upper left
        for n in range(1, min(row, col) + 1):
            if _is_seat(self.seats[row - n][col - n]):
                adj.append(self.seats[row - n][col - n])
                break
        # upper right
        for n in range(1, min(row + 1, len(self.seats[0]) - col)):
            if _is_seat(self.seats[row - n][col + n]):
                adj.append(self.seats[row - n][col + n])
                break
        # lower left
        for n in range(1, min(len(self.seats) - row, col + 1)):
            if _is_seat(self.seats[row + n][col - n]):
                adj.append(self.seats[row + n][col - n])
                break
        # lower right
        for n in range(1, min(len(self.seats) - row, len(self.seats[0]) - col)):
            if _is_seat(self.seats[row + n][col + n]):
                adj.append(self.seats[row + n][col + n])
                break
        return adj

    def adjacent_seats_empty(self, row, col, mode="adjacent"):
        """ return true iff 0 adjacent seats are occupied """
        if mode == "adjacent":
            get_seats = self._get_adjacent_seats
        elif mode == "nearest":
            get_seats = self._get_nearest_seats
        return get_seats(row, col).count("#") == 0

    def adjacent_seats_occupied(self, row, col, n=4, mode="adjacent"):
        """ return true iff n more adjacent seats are occupied """
        if mode == "adjacent":
            get_seats = self._get_adjacent_seats
        elif mode == "nearest":
            get_seats = self._get_nearest_seats
        # import pdb; pdb.set_trace()
        return get_seats(row, col).count("#") >= n

    def get_new_seat_val(self, row, col, n=4, mode="adjacent"):
        """ return new seat value """
        if self.seats[row][col] == "L" and self.adjacent_seats_empty(row, col, mode):
            # never fires
            return "#"
        if self.seats[row][col] == "#" and self.adjacent_seats_occupied(row, col, n, mode):
            return "L"

        return self.seats[row][col]

    def print_seats(self):
        for row in self.seats:
            print(row)

    def update(self, n=4, mode="adjacent"):
        s = ["".join([self.get_new_seat_val(r, c, n, mode) for c in range(len(self.seats[0]))])
                for r in range(len(self.seats))]
        self.seats = s

    def simulate(self, n=4, mode="adjacent"):
        loop = 0
        # print(f"\nloop {loop}")
        # self.print_seats()
        old = copy(self.seats)
        self.update(n, mode)
        loop += 1
        # print(f"\nloop {loop}")
        # self.print_seats()
        # loop until seats reach steady state
        while self.seats != old:
            # import pdb; pdb.set_trace()
            loop +=1
            old = copy(self.seats)
            self.update(n, mode)
            # print(f"\nloop {loop}")
            # self.print_seats()
        return sum([row.count("#") for row in self.seats])


if __name__ == "__main__":
    w = WaitingArea("inputs/day11_test.txt")
    print(f"day 11 part1 test: {w.simulate()}")
    w = WaitingArea("inputs/day11_test.txt")
    print(f"day 11 part2 test: {w.simulate(n=5, mode='nearest')}")
    w = WaitingArea("inputs/day11.txt")
    print(f"day 11 part1: {w.simulate()}")
    w = WaitingArea("inputs/day11.txt")
    print(f"day 11 part2: {w.simulate(n=5, mode='nearest')}")
