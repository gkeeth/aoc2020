#! /usr/bin/env python
import re

class Ferry(object):
    direction = {
            "E": (1, 0),
            "W": (-1, 0),
            "N": (0, -1),
            "S": (0, 1)
            }
    next_rotation = {
            # current direction: (right direction, left direction)
            "E": ("S", "N"),
            "S": ("W", "E"),
            "W": ("N", "S"),
            "N": ("E", "W")
            }
    def __init__(self, input_filename):
        self.dir = "E"
        self.x = 0
        self.y = 0
        self.wx = 10
        self.wy = -1
        with open(input_filename, "r") as infile:
            self.instructions = [line.strip() for line in infile]

    def get_manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def move(self, direction, distance):
        self.x += self.direction[direction][0] * distance
        self.y += self.direction[direction][1] * distance

    def rotate(self, direction, angle):
        if direction == "R":
            d = 0
        elif direction == "L":
            d = 1
        for _ in range(angle // 90):
            self.dir = self.next_rotation[self.dir][d]

    def move_waypoint(self, direction, distance):
        self.wx += self.direction[direction][0] * distance
        self.wy += self.direction[direction][1] * distance

    def move_to_waypoint(self, n):
        self.x += self.wx * n
        self.y += self.wy * n

    def rotate_waypoint(self, direction, angle):
        for _ in range(angle // 90):
            if direction == "R":
                wx = self.wx
                self.wx = -self.wy
                self.wy = wx
            elif direction == "L":
                wx = self.wx
                self.wx = self.wy
                self.wy = -wx

    def _execute_simple(self, inst, dist):
        if inst == "F":
            self.move(self.dir, dist)
        elif inst in "NSEW":
            self.move(inst, dist)
        elif inst in "RL":
            self.rotate(inst, dist)

    def _execute_waypoint(self, inst, dist):
        if inst == "F":
            self.move_to_waypoint(dist)
        elif inst in "NSEW":
            self.move_waypoint(inst, dist)
        elif inst in "RL":
            self.rotate_waypoint(inst, dist)

    def execute(self, instruction, mode="simple"):
        match = re.match("^([A-Z])(\d+)$", instruction)
        inst = match.group(1)
        dist = int(match.group(2))
        if mode == "simple":
            self._execute_simple(inst, dist)
        elif mode == "waypoint":
            self._execute_waypoint(inst, dist)

    def run(self, mode="simple"):
        for i in self.instructions:
            self.execute(i, mode)
        return self.get_manhattan_distance()


if __name__ == "__main__":
    f = Ferry("inputs/day12_test.txt")
    print(f"day 12a test: {f.run()}")
    f = Ferry("inputs/day12_test.txt")
    print(f"day 12b test: {f.run(mode='waypoint')}")
    f = Ferry("inputs/day12.txt")
    print(f"day 12a: {f.run()}")
    f = Ferry("inputs/day12.txt")
    print(f"day 12b: {f.run(mode='waypoint')}")
