#! /usr/bin/env python
from collections import defaultdict

class Floor(object):
    """
    Represent a hexagonal tiled floor in a cubic coordinate system:
        (0, +1, -1)         (+1, 0, -1)

    (-1, +1, 0)    (0, 0, 0)    (+1, -1, 0)

        (-1, 0, +1)         (0, -1, +1)
    """

    def __init__(self, input_filename):
        self.transform = {
                "e" : (+1, -1, 0),
                "se": (0, -1, +1),
                "sw": (-1, 0, +1),
                "w" : (-1, +1, 0),
                "nw": (0, +1, -1),
                "ne": (+1, 0, -1)
                }

        # map (x, y, z) cube coordinates -> color
        self.map = defaultdict(lambda: "white")

        self.black_tiles = 0

        with open(input_filename, "r") as infile:
            self.instructions = []
            for line in infile:
                edges = []
                line = line.strip()
                while line:
                    if line.startswith("s") or line.startswith("n"):
                        edges.append(line[0:2])
                        line = line[2:]
                    elif line.startswith("e") or line.startswith("w"):
                        edges.append(line[0])
                        line = line[1:]
                    else:
                        print(f"error parsing line: {line}")
                        break
                self.instructions.append(edges)

    def flip(self, xyz):
        if self.map[xyz] == "white":
            self.map[xyz] = "black"
            self.black_tiles += 1
            # make sure all neighbors are initialized
            x, y, z = xyz
            for t in self.transform.values():
                if (x + t[0], y + t[1], z + t[2]) not in self.map:
                    self.map[(x + t[0], y + t[1], z + t[2])] = "white"
        elif self.map[xyz] == "black":
            self.map[xyz] = "white"
            self.black_tiles -= 1

    def flip_tiles(self):
        for instruction in self.instructions:
            coord = (0, 0, 0)
            for edge in instruction:
                dx, dy, dz = self.transform[edge]
                coord = (coord[0] + dx, coord[1] + dy, coord[2] + dz)
            self.flip(coord)
        return self.black_tiles

    def get_neighbors(self, xyz):
        x, y, z = xyz
        return [self.map[(x + t[0], y + t[1], z + t[2])]
                for t in self.transform.values()]

    def update(self):
        """
        simultaneously update all tiles:
        - black tiles with 0 or more than 2 adjacent black tiles are flipped to white
        - white tiles with 2 adjacent black tiles are flipped to black
        """
        to_be_flipped = []
        coords = list(self.map.keys())
        for xyz in coords:
            neighbors = self.get_neighbors(xyz)
            black_tiles = neighbors.count("black")
            if self.map[xyz] == "black" and (black_tiles == 0 or black_tiles > 2):
                to_be_flipped.append(xyz)
            elif self.map[xyz] == "white" and black_tiles == 2:
                to_be_flipped.append(xyz)

        for xyz in to_be_flipped:
            self.flip(xyz)

    def exhibit(self, days=10):
        # print(f"initially: {self.black_tiles}")
        for n in range(days):
            self.update()
            # print(f"Day {n+1}: {self.black_tiles}")
        return self.black_tiles

    @staticmethod
    def cube_to_offset(xyz):
        """ odd rows shifted by +1/2 column """
        x, y, z = xyz
        col = x + (z - (z % 2)) // 2
        row = z
        return col, row

    @staticmethod
    def offset_to_cube(row, col):
        x = col - (row - (row % 2)) // 2
        z = row
        y = -x - z
        return x, y, z

    def print(self):
        rows = [Floor.cube_to_offset(xyz)[1] for xyz in self.map]
        cols = [Floor.cube_to_offset(xyz)[0] for xyz in self.map]
        rowmin = min(rows + [0])
        rowmax = max(rows + [0])
        colmin = min(cols + [0])
        colmax = max(cols + [0])
        print(f"top left: {colmin, rowmin}")
        print(f"bottom right: {colmax, rowmax}")

        for r in range(rowmin, rowmax + 1):
            s = ""
            if r % 2:
                # draw odd rows offset to right
                s += " "
            for c in range(colmin, colmax + 1):
                if self.map[Floor.offset_to_cube(r, c)] == "black":
                    s += "# "
                else:
                    s += ". "
            print(s)


if __name__ == "__main__":
    f = Floor("inputs/day24_test.txt")
    print(f"day24a test: {f.flip_tiles()}")
    print(f"day24b test: {f.exhibit(days=100)}")
    f = Floor("inputs/day24.txt")
    print(f"day24a: {f.flip_tiles()}")
    print(f"day24b: {f.exhibit(days=100)}")
