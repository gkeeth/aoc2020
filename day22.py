#! /usr/bin/env python
from copy import deepcopy

class SpaceCards(object):
    def __init__(self, input_filename):
        self.decks = {}
        with open(input_filename, "r") as infile:
            for line in infile:
                if "Player" in line:
                    player = int(line.replace(":", "").split()[1])
                    cards = []
                elif line.strip() == "":
                    self.decks[player] = cards
                else:
                    cards.insert(0, int(line))
            self.decks[player] = cards

    def play_round(self):
        card1 = self.decks[1].pop()
        card2 = self.decks[2].pop()
        if card1 > card2:
            self.decks[1].insert(0, card1)
            self.decks[1].insert(0, card2)
        else:
            self.decks[2].insert(0, card2)
            self.decks[2].insert(0, card1)

    def play_game(self):
        while len(self.decks[1]) > 0 and len(self.decks[2]) > 0:
            self.play_round()

        if len(self.decks[1]) == 0:
            winner = self.decks[2]
        else:
            winner = self.decks[1]

        score = 0
        for n, value in enumerate(winner, start=1):
            score += n * value

        return score

    def _play_game_recursive(self, game):
        prev_states1 = []
        prev_states2 = []
        while True:
            if game.decks[1] in prev_states1 or game.decks[2] in prev_states2:
                return 1, game # player 1 wins game
            # prev_states.append(deepcopy(game.decks))
            prev_states1.append(deepcopy(game.decks[1]))
            prev_states2.append(deepcopy(game.decks[2]))

            card1 = game.decks[1].pop()
            card2 = game.decks[2].pop()
            if len(game.decks[1]) >= card1 and len(game.decks[2]) >= card2:
                newgame = deepcopy(game)
                newgame.decks[1] = newgame.decks[1][-card1:]
                newgame.decks[2] = newgame.decks[2][-card2:]
                winner, _ = game._play_game_recursive(newgame)
            else:
                # winner is player with higher-valued card
                if card1 > card2:
                    winner = 1
                else:
                    winner = 2

            if winner == 1:
                game.decks[1].insert(0, card1)
                game.decks[1].insert(0, card2)
            else:
                game.decks[2].insert(0, card2)
                game.decks[2].insert(0, card1)

            if len(game.decks[1]) == 0:
                return (2, game) # player 2 wins
            elif len(game.decks[2]) == 0:
                return (1, game) # player 1 wins

    def play_game_recursive(self):
        winner, game = self._play_game_recursive(deepcopy(self))
        score = 0
        for n, value in enumerate(game.decks[winner], start=1):
            score += n * value
        return score



if __name__ == "__main__":
    s = SpaceCards("inputs/day22_test.txt")
    print(f"day22a test: {s.play_game()}")
    s = SpaceCards("inputs/day22.txt")
    print(f"day22a: {s.play_game()}")
    s = SpaceCards("inputs/day22_test.txt")
    print(f"day22b test: {s.play_game_recursive()}")
    s = SpaceCards("inputs/day22_recursion_test.txt")
    print(f"day22b recursion test: {s.play_game_recursive()}")
    s = SpaceCards("inputs/day22.txt")
    print(f"day22b: {s.play_game_recursive()}")
