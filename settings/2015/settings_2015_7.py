from functools import lru_cache
from operator import and_, lshift, or_, rshift, not_
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> a
NOT y -> i
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_7_1.txt"

parse_input = lambda data: {(s := line.split(' -> '))[1]: s[0].split() for line in data}

def get_value(wires, wire='a', set_wire={}):
    operations = {'AND': and_, 'OR': or_, 'LSHIFT': lshift, 'RSHIFT': rshift}

    @lru_cache(512)
    def aux(wire):
        # already computed?
        try:
            return int(wire)
        except:
            lhs = wires[wire]
            match len(lhs):
                case 1: # affectation
                    return aux(lhs[0])
                case 2: # not_
                    return ~aux( lhs[1]) & 0xFFFF
                case 3:
                    return operations[lhs[1]](aux(lhs[0]), aux(lhs[2]))
            
    if set_wire:
        wires |= set_wire
    return aux(wire)

def exo1(data: list[str]) -> int:
    return get_value(parse_input(data))

# >> 956
def exo2(data: list[str]) -> Any:
    return get_value(parse_input(data), set_wire={'b': [956]})

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 65412,
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
            'expected': 65412,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)