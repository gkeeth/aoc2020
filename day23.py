#! /usr/bin/env python

class Game(object):
    def __init__(self, input_string, version=1):
        cups = [int(n) for n in input_string]
        if version == 2:
            cups.extend(range(max(cups) + 1, 1000001))
        self.cups = {cups[n]: cups[(n+1) % len(cups)] for n in range(len(cups))}
        self.current = cups[0]
        self.version = version
        self.min = min(cups)
        self.max = max(cups)

    def print_cups(self):
        c = []
        n = self.current
        for _ in range(len(self.cups)):
            c.append(str(n))
            n = self.cups[n]
        print(" ".join(c))


    def play_move(self):
        # remove the 3 cups after current
        cup1 = self.cups[self.current]
        cup2 = self.cups[cup1]
        cup3 = self.cups[cup2]
        removed = [cup1, cup2, cup3]
        self.cups[self.current] = self.cups[cup3]

        # pick a destination for removed cups
        dest = self.current - 1
        if dest < self.min:
            dest = self.max
        while dest in removed:
            dest -= 1
            if dest < self.min:
                dest = self.max

        # insert the 3 removed cups after dest_index
        self.cups[cup3] = self.cups[dest]
        self.cups[dest] = cup1

        # choose new current cup
        self.current = self.cups[self.current]

    def play(self, rounds=100):
        for n in range(rounds):
            self.play_move()

        if self.version == 1:
            # result should be formatted with the cups in order, starting after "1"
            cups = []
            n = self.cups[1]
            for _ in range(len(self.cups) - 1):
                cups.append(str(n))
                n = self.cups[n]
            return "".join(cups)
        elif self.version == 2:
            print(f"cup 1: {self.cups[1]}")
            print(f"cup 2: {self.cups[self.cups[1]]}")
            return self.cups[1] * self.cups[self.cups[1]]

if __name__ == "__main__":
    g = Game("389125467")
    print(f"day23a test: {g.play(rounds=10)}")
    g = Game("389125467")
    print(f"day23a test2: {g.play(rounds=100)}")
    g = Game("653427918")
    print(f"day23a: {g.play(rounds=100)}")
    g = Game("389125467", version=2)
    print(f"day23b test: {g.play(rounds=10000000)}")
    g = Game("653427918", version=2)
    print(f"day23b: {g.play(rounds=10000000)}")
