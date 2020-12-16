#! /usr/bin/env python
import math

class BusSchedule(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            f = infile.readlines()
            self.t0 = int(f[0])
            self.buses = [int(b) for b in f[1].split(",") if b != "x"]
            self.bus_constraints = [b for b in f[1].split(",")]

    def find_earliest_bus(self):
        times = [(math.ceil(self.t0 / bus) * bus, bus) for bus in self.buses]
        soonest = times[0]
        for time, bus in times:
            if time < soonest[0]:
                soonest = (time, bus)
        return (soonest[0] - self.t0) * soonest[1]

    def win_contest(self):
        buses = [(int(bus), offset)
                for offset, bus in enumerate(self.bus_constraints)
                if bus != "x"]
        t = 0
        step = 1

        for bus, offset in buses:
            while (t + offset) % bus:
                t += step
            # found a time that works for all buses checked so far.
            # this is new minimum interval for searching next buses
            step *= bus
        return t

if __name__ == "__main__":
    b = BusSchedule("inputs/day13_test.txt")
    print(f"day 13a test: {b.find_earliest_bus()}")
    print(f"day 13b test: {b.win_contest()}")
    b = BusSchedule("inputs/day13.txt")
    print(f"day 13a: {b.find_earliest_bus()}")
    print(f"day 13b: {b.win_contest()}")


