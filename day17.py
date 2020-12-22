#! /usr/bin/env python

from collections import defaultdict
import itertools

class Pocket(object):
    def __init__(self, input_filename, dimensions=3):
        # (x, y, z, [w]) -> "#"
        self.dimensions = dimensions
        self.active_cubes = {}
        with open(input_filename, "r") as infile:
            for y, line in enumerate(infile):
                for x, c in enumerate(line.strip()):
                    if c == "#":
                        if dimensions == 3:
                            self.active_cubes[(x, y, 0)] = "#"
                        elif dimensions == 4:
                            self.active_cubes[(x, y, 0, 0)] = "#"


    def get_neighbors(self, x, y, z, w=0):
        """ return list of (x,y,z[,w]) coordinates of all 26 (3D) or 80 (4D) neighbors """
        if self.dimensions == 3:
            neighbors = list(itertools.product((x-1, x, x+1), (y-1, y, y+1), (z-1, z, z+1)))
            neighbors.remove((x, y, z))
        elif self.dimensions == 4:
            neighbors = list(itertools.product((x-1, x, x+1), (y-1, y, y+1), (z-1, z, z+1), (w-1, w, w+1)))
            neighbors.remove((x, y, z, w))

        return neighbors

    def print(self):
        # count number of z levels
        x_indices = sorted(set([c[0] for c in self.active_cubes]))
        y_indices = sorted(set([c[1] for c in self.active_cubes]))
        z_indices = sorted(set([c[2] for c in self.active_cubes]))
        if self.dimensions == 3:
            w_indices = [0]
        elif self.dimensions == 4:
            w_indices = sorted(set([c[3] for c in self.active_cubes]))
        for w in w_indices:
            for z in z_indices:
                print(f"\nz={z}, w={w}")
                for y in y_indices:
                    print("".join(["#" if (x, y, z) in self.active_cubes else "."
                        for x in x_indices]))

    def update(self):
        next_active_cubes = {}
        for active in self.active_cubes:
            neighbors = self.get_neighbors(*active)
            active_neighbors = [c for c in neighbors
                    if c in self.active_cubes]
            inactive_neighbors = [c for c in neighbors
                    if c not in self.active_cubes]

            # active cubes with 2 or 3 active neighbors stay active. Otherwise,
            # they become inactive.
            if len(active_neighbors) == 2 or len(active_neighbors) == 3:
                next_active_cubes[active] = "#"

            # inactive cubes with 3 active neighbors become active
            for inactive in inactive_neighbors:
                neighbors_of_inactive = self.get_neighbors(*inactive)
                active_neighbors_of_inactive = [c for c in neighbors_of_inactive
                        if c in self.active_cubes]
                if len(active_neighbors_of_inactive) == 3:
                    next_active_cubes[inactive] = "#"

        # update the coords
        self.active_cubes = next_active_cubes

    def run(self, rounds=6):
        print("Before any cycles:\n")
        self.print()
        for n in range(rounds):
            self.update()
            print(f"\nAfter {n+1} cycles:")
            self.print()
        # count active cubes
        return len(self.active_cubes)


if __name__ == "__main__":
    p = Pocket("inputs/day17_test.txt")
    print(f"day17 test1: {p.run()}")
    p = Pocket("inputs/day17.txt")
    print(f"day17 part1: {p.run()}")
    p = Pocket("inputs/day17_test.txt", dimensions=4)
    print(f"day17 test2: {p.run()}")
    p = Pocket("inputs/day17.txt", dimensions=4)
    print(f"day17 part2: {p.run()}")


