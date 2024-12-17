import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_1 = """
H => HO
H => OH
O => HH

HOHOHO
"""
#HOH
TEST_DATA_2 = """
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_19_1.txt"

def parse_input(data: str, revert: bool = False) -> tuple[str, dict[str: set[str]]]:
    _d, l = data.strip().split('\n\n')
    d = {}
    for line in _d.strip().split('\n'):
        k, v = line.split(' => ')
        if revert:
            d[v] = k
        else:
            d.setdefault(k, set()).add(v)
    return l, d


class Machine:
    def __init__(self, data: str):
        self.chain, self.subst = parse_input(data)
        self.re_sub = re.compile(r'|'.join(list(set(self.subst.keys()))))

    def substitutions(self):
        for curm in self.re_sub.finditer(self.chain):
            curs = curm.group()
            for s in self.subst.get(curs, (curs)):
                yield ''.join(self.chain[:curm.start()] + s + self.chain[curm.end():])


class Synthetizer:
    def __init__(self, data: str):
        self.chain, self.subst = parse_input(data, True)

    

def exo1(data: str) -> int:
    m = Machine(data)
    s = set(m.substitutions())
    return len(s)

def exo2(data: str) -> int:
    s = Synthetizer(data)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 7,
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
            'expected': 6,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)