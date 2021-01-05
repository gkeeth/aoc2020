#! /usr/bin/env python
from itertools import combinations
from functools import reduce
from collections import defaultdict
import math
import re

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

    @staticmethod
    def rotate(m):
        """ rotate map 90deg clockwise """
        rotated = []
        for n in range(len(m)):
            rotated.append("".join([row[n] for row in m[::-1]]))
        return rotated

    @staticmethod
    def flipx(m):
        """ flip map vertically (mirror across x axis) """
        return m[::-1]


    def measure_roughness(self):
        """
        1. assemble tiles into map
        2. strip edges
        3. count sea monsters in map
        4. measure roughness of seas
        """
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
                            if ("left" in matching_edges and matching_edges["left"] == prev.id_num
                                    and "top" in matching_edges and matching_edges["top"] == upper.id_num):
                                break
                    t()
                    # transforming matching_edges would be cheaper than recalculating...
                    matching_edges = tile.get_matching_edges(self.tiles.values())
                m[row][n] = tile.id_num

        m = [list(map("".join, zip(*[self.tiles[id_num].strip_edges() for id_num in row]))) for row in m]
        m = [col for block in m for col in block]

        # search for sea creatures
        # sea creatures look like:
        # __________________#_
        # #____##____##____###
        # _#__#__#__#__#__#___
        #
        # sea creatures contain 15 '#'es
        monster1 = "..................#."
        monster1 = "#" # preceded by 18 chars, succeeded by 1
        monster2 = "#....##....##....###"
        monster3 = ".#..#..#..#..#..#..."
        transforms = [self.rotate, self.rotate, self.rotate, self.flipx, self.rotate, self.rotate, self.rotate, lambda a: a]
        for t in transforms:
            monsters = 0
            for l, line in enumerate(m):
                for match1 in re.finditer(monster1, line[18:len(m)-1]):
                    if l + 2 < len(m):
                        prefix = "." * match1.start()
                        match2 = re.match(prefix + monster2, m[l+1])
                        if match2:
                            match3 = re.match(prefix + monster3, m[l+2])
                            if match3:
                                monsters += 1
            if monsters > 0:
                break
            else:
                m = t(m)

        # count number of '#' chars in m, and subtract those contained in
        # monsters to measure roughness of sea
        return "".join(m).count("#") - monsters * 15




if __name__ == "__main__":
    t = TileMap("inputs/day20_test.txt")
    print(f"day 20 test: {t.multiply_corner_ids()}")
    print(f"day 20b test: {t.measure_roughness()}")
    t = TileMap("inputs/day20.txt")
    print(f"day 20a: {t.multiply_corner_ids()}")
    print(f"day 20b: {t.measure_roughness()}")

