from itertools import combinations
from math import prod


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
1
2
3
4
5
7
8
9
10
11
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2015_24.txt"

class GiftPackager:
    def __init__(self, data: list[str], parts: int) -> None:
        self.gifts = [int(g) for g in data]
        self.parts = parts
        self.target_weight = sum(self.gifts) // self.parts

    def minimal_packages(self) -> list[tuple]:
        for nbp in range(1, len(self.gifts) // self.parts + 1):
            if valid := [combo for combo in list(combinations(self.gifts, nbp)) if sum(combo) == self.target_weight]:
                return valid
        raise ValueError('No combo found')

    def best(self) -> int:
        return min(prod(combo) for combo in self.minimal_packages())


def exo1(data: list[str]) -> int:
    return GiftPackager(data, 3).best()

def exo2(data: list[str]) -> int:
    return GiftPackager(data, 4).best()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 99,
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
            'expected': 44,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
