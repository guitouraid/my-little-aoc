from itertools import chain, combinations
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
20
15
10
5
5
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_17_1.txt"

class Containers:
    def __init__(self, data: str, target: int):
        self.containers = [int(v) for v in data.split('\n') if v]
        self.target = target

    def powerset(self):
        s = list(range(len(self.containers)))
        return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))

    def checksum(self, t: tuple) -> bool:
        return sum(self.containers[i] for i in t) == self.target
    
    def lchecksum(self, t: tuple) -> list[int]:
        if self.checksum(t):
            return len(t)

def exo1(data: str, total: int) -> int:
    c = Containers(data, total)
    return sum(
        c.checksum(t)
        for t in c.powerset()
    )

def exo2(data: str, total: int) -> int:
    c = Containers(data, total)
    ls = [s for s in map(lambda t: c.lchecksum(t), c.powerset()) if s]
    return ls.count(min(ls))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 4,
            'kw_args': {'total': 25},
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
            'kw_args': {'total': 150},
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 3,
            'kw_args': {'total': 25},
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
            'kw_args': {'total': 150},
        },
        'runner': exo2,
    },
)