#! /usr/bin/env python
import functools

class TobogganMap(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            self.map = [line.strip() for line in infile]
        self.width = len(self.map[0])

    def get_value(self, startx, starty, right, down):
        """ get value of map at position (startx + right, starty + down) """
        return self.map[starty + down][(startx + right) % self.width]

    def count_trees(self, right, down):
        """ count trees hit by starting at (0, 0) and traveling with slope specified by right, down """
        x = 0
        y = 0
        trees = 0
        while y + down < len(self.map):
            if self.get_value(x, y, right, down) == "#":
                trees += 1
            x += right
            y += down
        return trees

    def get_answer(self, slopes):
        """
        multiply together obstacles found for each of the slopes in slopes

        list_of_slopes: list of tuples (right, down).
        """
        obstacles = [self.count_trees(s[0], s[1]) for s in slopes]
        return functools.reduce(lambda a, b: a * b, obstacles)

if __name__ == "__main__":
    m = TobogganMap("inputs/day3_test.txt")
    print("Day 3 test: {}".format(m.get_answer([(3, 1)])))
    m = TobogganMap("inputs/day3.txt")
    print("Day 3a: {}".format(m.get_answer([(3, 1)])))
    print("Day 3b: {}".format(m.get_answer([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])))
