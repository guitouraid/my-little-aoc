from functools import reduce
from itertools import combinations
from operator import mul
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
2x3x4
1x1x10
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_2_1.txt"

def parse_line(line: str) -> list[int]:
    return list(map(lambda s: int(s), line.split('x')))

def paper(dims: list[int]) -> int:
    faces = list(map(lambda t: t[0]*t[1], combinations(dims, 2)))
    return min(faces) + 2*sum(faces)

def ribbon(dims: list[int]) -> int:
    bow = reduce(mul, dims)
    dims.remove(max(dims))
    return bow + 2*sum(dims)

def exo1(data: list[str]) -> Any:
    return sum([paper(parse_line(line)) for line in data])

def exo2(data: list[str]) -> Any:
    return sum([ribbon(parse_line(line)) for line in data])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 101,
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
            'expected': 48,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)