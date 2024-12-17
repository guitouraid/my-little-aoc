from itertools import permutations
import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_13_1.txt"

RE_LINE = re.compile(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).')
MULTI = {
    'gain': 1,
    'lose': -1,
}

def read_lines(data: list[str]) -> dict[str:dict[str:int]]:
    d = {}
    for line in data:
        if not (m := RE_LINE.match(line)):
            raise ValueError(f'Invalid line: {line}')
        a, sign, val, b = m.groups()
        d.setdefault(a, {})[b] = MULTI[sign]*int(val)
    return d

def solve(scores: dict) -> int:
    return max(
        sum(scores[a][b] + scores[b][a] for a, b in zip(l, list(l[1:]) + [l[0]]))
        for l in permutations(scores.keys())
    )

def cheat(scores: dict[str:dict[str:int]]) -> dict[str:dict[str:int]]:
    me = {}
    for p, d in scores.items():
        scores[p]['me'] = 0
        me[p] = 0
    return scores | {'me': me}

def exo1(data: list[str]) -> int:
    return solve(read_lines(data))

def exo2(data: list[str]) -> int:
    return solve(cheat(read_lines(data)))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 330,
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
            'expected': 0,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)