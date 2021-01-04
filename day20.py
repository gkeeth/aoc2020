#! /usr/bin/env python
from itertools import combinations
from functools import reduce
from collections import defaultdict
import math

class Tile(object):
    def __init__(self, id_num, data):
        self.id_num = id_num
        self.data = data

    def get_edges(self):
        """ return dict of edge name to edge data """
        return {
                "top": self.data[0],
                "bottom": self.data[-1],
                "left": "".join(row[0] for row in self.data),
                "right": "".join(row[-1] for row in self.data)
                }

    def strip_edges(self):
        """ return data with edges removed """
        return [row[1:-1] for row in self.data[1:-1]]

    def get_matching_edges(self, others):
        """ return dict of edge name to id of tile it matches with """
        matching_edges = {}
        for edge_name, edge in self.get_edges().items():
            for other in others:
                if other == self:
                    continue
                for other_edge in other.get_edges().values():
                    if edge == other_edge or edge == other_edge[::-1]:
                        matching_edges[edge_name] = other.id_num
        return matching_edges

    def has_matching_edge(self, other):
        """ return True iff an edge of `self` lines up with an edge of `other` """
        for edge in self.get_edges().values():
            for other_edge in other.get_edges().values():
                if edge == other_edge or edge == other_edge[::-1]:
                    return True
        return False

    def rotate(self):
        """ rotate tile 90deg clockwise """
        rotated = []
        for n in range(len(self.data)):
            rotated.append("".join([row[n] for row in self.data[::-1]]))
        self.data = rotated

    def flipx(self):
        """ flip tile vertically (mirror across x axis) """
        self.data.reverse()


class TileMap(object):
    def __init__(self, input_filename):
        self.tiles = {}
        with open(input_filename, "r") as infile:
            for line in infile:
                if "Tile" in line:
                    id_num = int(line.split()[1].replace(":", ""))
                    data = []
                elif "#" in line or "." in line:
                    data.append(line.strip())
                else:
                    self.tiles[id_num] = Tile(id_num, data)
            self.tiles[id_num] = Tile(id_num, data)

    def count_matching_edges(self):
        """ return dict of id_nums -> # of edges that match another tile's edge """
        matching_edges = defaultdict(int)
        for (tile, other) in combinations(self.tiles.keys(), 2):
            if self.tiles[tile].has_matching_edge(self.tiles[other]):
                matching_edges[tile] += 1
                matching_edges[other] += 1
        return matching_edges


    def find_corner_tiles(self):
        """
        return list of id_nums of corner tiles (tiles with 2 edges that match
        with edges on other tiles)
        """
        matching_edges = self.count_matching_edges()
        return [id_num for id_num in matching_edges if matching_edges[id_num] == 2]

    def multiply_corner_ids(self):
        return reduce((lambda a, b: a * b), self.find_corner_tiles())

    def assemble_image(self):
        row_len = int(math.sqrt(len(self.tiles)))
        m = [[None for _ in range(row_len)] for _ in range(row_len)]
        corners = self.find_corner_tiles()

        for row in range(row_len):
            for n in range(row_len):
                if n == 0:
                    if row == 0:
                        # choose top left tile arbitrarily
                        tile = self.tiles[corners[0]]
                    else:
                        # first tile in row is below first tile in previous row
                        upper = self.tiles[m[row-1][0]]
                        tile = self.tiles[upper.get_matching_edges(self.tiles.values())["bottom"]]
                else:
                    prev = tile
                    tile = self.tiles[matching_edges["right"]]
                    if row != 0:
                        upper = self.tiles[upper.get_matching_edges(self.tiles.values())["right"]]

                # transform until unmatched edge is on top, and left edges matches with previous tile
                matching_edges = tile.get_matching_edges(self.tiles.values())
                transforms = [tile.rotate, tile.rotate, tile.rotate, tile.flipx, tile.rotate, tile.rotate, tile.rotate]
                for t in transforms:
                    if row == 0:
                        if n == 0:
                            if "right" in matching_edges and "bottom" in matching_edges:
                                break
                        else:
                            if "top" not in matching_edges and "left" in matching_edges and matching_edges["left"] == prev.id_num:
                                break
                    else:
                        if n == 0:
                            if "left" not in matching_edges and "top" in matching_edges and matching_edges["top"] == upper.id_num:
                                break
                        else:
                            if "left" in matching_edges and matching_edges["left"] == prev.id_num and matching_edges["top"] == upper.id_num:
                                break
                    t()
                    # transforming matching_edges would be cheaper than recalculating...
                    matching_edges = tile.get_matching_edges(self.tiles.values())
                m[row][n] = tile.id_num
        print(m)
        stripped_m = [list(map("".join, zip(*[self.tiles[id_num].strip_edges() for id_num in row]))) for row in m]
        print(stripped_m)


if __name__ == "__main__":
    t = TileMap("inputs/day20_test.txt")
    print(f"day 20 test: {t.multiply_corner_ids()}")
    print(f"matching edges in 2311: {t.tiles[2311].get_matching_edges(t.tiles.values())}")
    t.assemble_image()
    t = TileMap("inputs/day20.txt")
    print(f"day 20a: {t.multiply_corner_ids()}")

