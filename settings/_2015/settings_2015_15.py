from collections import Counter
from itertools import combinations_with_replacement, permutations, product
from math import prod
import re

from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_15_1.txt"

INGREDIENTS = 100
CALORIES = 500
RE_NUM = re.compile(r'-?\d+')

class Ingredient:
    def __init__(self, t: tuple):
        self.t = t
        self.len = len(self.t)-1

    def calories(self, q: int) -> int:
        return self.t[self.len]*q

    def props(self, q: int) -> tuple:
        return tuple(self.t[i]*q for i in range(self.len))


class Recipe:
    def __init__(self, ingredients: list[Ingredient], counter: Counter):
        self.ingredients = ingredients
        self.counter = counter
        self.len = len(self.ingredients)
        self.ilen = self.ingredients[0].len

    @property
    def props(self) -> list[tuple]:
        return tuple(
            map(
                sum,
                zip(
                    *map(lambda i: self.ingredients[i].props(self.counter[i]), range(self.len))
                )
            )
        )
    
    @property
    def calories(self) -> int:
        return sum(self.ingredients[i].calories(self.counter[i]) for i in range(self.len))

    @property
    def prod(self) -> int:
        return prod(max(0, v) for v in self.props)

    @property
    def calprod(self) -> int:
        if self.calories == CALORIES:
            return self.prod
        return 0


class Recipes:
    def __init__(self, data: list[str]):
        self.ingredients = [
            Ingredient(
                tuple(
                    map(int, RE_NUM.findall(line))
                )
            )
            for line in data
        ]
        self.len = len(self.ingredients)
        self.ilen = self.ingredients[0].len
        self.combos = set(
            perm
            for combo in combinations_with_replacement(range(1, INGREDIENTS), self.len)
                if sum(combo) == INGREDIENTS
            for perm in permutations(combo)
        )

    @property
    def best(self) -> int:
        return max(
            Recipe(self.ingredients, Counter({i: c[i] for i in range(self.len)})).prod
            for c in self.combos
        )

    @property
    def bestcal(self) -> int:
        return max(
            Recipe(self.ingredients, Counter({i: c[i] for i in range(self.len)})).calprod
            for c in self.combos
        )


def exo1(data: list[str]) -> int:
    return Recipes(data).best

def exo2(data: list[str]) -> int:
    return Recipes(data).bestcal

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 62842880,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 57600000,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)