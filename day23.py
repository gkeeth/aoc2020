#! /usr/bin/env python

class Game(object):
    def __init__(self, input_string, version=1):
        self.cups = [int(n) for n in input_string]
        self.current = 0 # index of current cup
        self.version = version
        if version == 2:
            # add additional numbers up to 1 million
            self.cups += range(max(self.cups), 1000001)

    def play_move(self):
        # import pdb; pdb.set_trace()
        # print(self.cups)
        # print(f"current index: {self.current}")
        # print(f"current: {self.cups[self.current]}")
        current_val = self.cups[self.current]
        # remove the 3 cups after current
        removed = []
        for _ in range(3):
            index = self.cups.index(current_val)
            removed.append(self.cups.pop((index + 1) % len(self.cups)))
        # print(f"pickup: {removed}")

        # pick a destination for removed cups
        dest = self.cups[self.cups.index(current_val)] - 1
        if dest < min(self.cups + removed):
            dest = max(self.cups + removed)
        while dest in removed:
            dest -= 1
            if dest < min(self.cups + removed):
                dest = max(self.cups + removed)
        dest_index = self.cups.index(dest)
        # print(f"destination: {dest} at {dest_index}")

        # insert the 3 removed cups after dest_index
        for n, cup in enumerate(removed):
            self.cups.insert(dest_index + 1 + n, cup)

        # choose new current cup
        self.current = (self.cups.index(current_val) + 1) % len(self.cups)

    @staticmethod
    def rotate(cups):
        """ right-shift list of cups and return rotated list """
        return cups[-1:] + cups[:-1]

    def play(self, rounds=100):
        for n in range(rounds):
            # print(f"-- move {n+1} --")
            self.play_move()
            # print()

        if self.version == 1:
            # result should be formatted with the cups in order, starting after "1"
            cups = [str(n) for n in self.cups]
            while cups[0] != "1":
                cups = Game.rotate(cups)
            return "".join(cups[1:])
        elif self.version == 2:
            index = self.cups.index(1)
            return (self.cups[(index + 1) % len(self.cups)]
                    * self.cups[(index + 2) % len(self.cups)])

if __name__ == "__main__":
    g = Game("389125467")
    print(f"day23a test: {g.play(rounds=10)}")
    g = Game("389125467")
    print(f"day23a test2: {g.play(rounds=100)}")
    g = Game("653427918")
    print(f"day23a: {g.play(rounds=100)}")
    g = Game("653427918", version=2)
    print(f"day23b: {g.play(rounds=10000000)}")
