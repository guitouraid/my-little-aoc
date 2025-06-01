from itertools import count
import re


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_15.txt"

RE_NUMBERS = re.compile(r'\d+')

class Disc:
    def __init__(self, rounds: int, start: int) -> None:
        self.rounds = rounds
        self.start = start

    def unaligned(self, sec: int) -> bool:
        return bool((self.start + sec) % self.rounds)

def parse_input(data: list[str]) -> list[Disc]:
    return [ Disc(int(rounds), int(start)) for (_, rounds, _, start) in map(RE_NUMBERS.findall, data)]

def min_sec(discs: list[Disc]) -> int:
    for sec in count():
        if any( d.unaligned(sec+j+1) for j, d in enumerate(discs)):
            continue
        return sec
    raise ValueError('Supposedly unreachable code')

def exo1(data: list[str]) -> int:
    discs = parse_input(data)
    return min_sec(discs)

def exo2(data: list[str]) -> int:
    discs = parse_input(data)
    discs.append(Disc(11,0))
    return min_sec(discs)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 5,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_1,
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
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
