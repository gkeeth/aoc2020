#! /usr/bin/env python
import re
from collections import defaultdict

class Food(object):
    def __init__(self, line):
            match = re.match("^(.*) \(contains (.*)\)$", line.replace(",", ""))
            self.ingredients = set(match.groups()[0].split())
            self.allergens = set(match.groups()[1].split())

class FoodList(object):
    def __init__(self, input_filename):
        with open(input_filename, "r") as infile:
            self.foods = [Food(line) for line in infile]
        self.allergens = set()
        for food in self.foods:
            self.allergens |= food.allergens

    def solve(self):
        """
        return dict of allergen -> ingredient
        """
        # allergen -> possible ingredients that contain that allergen (1 is true)
        candidates = {}
        for allergen in self.allergens:
            # get intersection of all foods that contain that allergen
            for food in self.foods:
                if allergen in food.allergens:
                    if allergen in candidates:
                        candidates[allergen] &= food.ingredients
                    else:
                        candidates[allergen] = food.ingredients.copy()

        # allergen -> {ingredient}
        solved_allergens = {}
        unsolved = True
        while unsolved:
            # if any allergens have only 1 candidate ingredient, that candidate
            # must be correct. Remove that candidate ingredient from all other
            # allergens.
            unsolved = False
            for allergen in candidates:
                if len(candidates[allergen]) == 1:
                    solved_allergens[allergen] = candidates[allergen]
                    for other_allergen in set(candidates.keys()) - set([allergen]):
                        candidates[other_allergen] -= solved_allergens[allergen]
                else:
                    unsolved = True

        return solved_allergens

    def get_unsafe_ingredients(self):
        """ return set of unsafe ingredients """
        solved_allergens = self.solve()
        unsafe_ingredients = set()
        for ingredient in solved_allergens.values():
            unsafe_ingredients |= ingredient
        return unsafe_ingredients

    def count_safe_ingredients(self):
        """
        find ingredients that can't contain any allergens, and count number of
        times they appear
        """
        unsafe_ingredients = self.get_unsafe_ingredients()

        all_ingredients = set()
        for food in self.foods:
            all_ingredients |= food.ingredients
        safe_ingredients = all_ingredients - unsafe_ingredients

        count = 0
        for food in self.foods:
            for ingredient in safe_ingredients:
                if ingredient in food.ingredients:
                    count += 1
        return count

    def list_unsafe_ingredients(self):
        """
        return comma-separated list of dangerous ingredients, sorted
        alphabetically by allergen
        """
        solved_allergens = self.solve() # allergen -> ingredient
        return ",".join([solved_allergens[allergen].pop() for allergen in sorted(solved_allergens.keys())])


if __name__ == "__main__":
    f = FoodList("inputs/day21_test.txt")
    print(f"day21a test: {f.count_safe_ingredients()}")
    print(f"day21b test: {f.list_unsafe_ingredients()}")
    f = FoodList("inputs/day21.txt")
    print(f"day21a: {f.count_safe_ingredients()}")
    print(f"day21a: {f.list_unsafe_ingredients()}")

