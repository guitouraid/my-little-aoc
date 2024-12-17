from itertools import permutations
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_9_1.txt"

def parse_line(line: str):
    a, _, b, _, d = line.split()
    return a, b, int(d)

def parse_input(data: list[str]):
    locations = set()
    distances = {}
    for a, b, d in map(parse_line, data):
        locations |= {a, b}
        distances[(a,b)] = distances[(b,a)] = d
    return locations, distances

solver = lambda f,d,l : (
    f(sum(d[trip] for trip in zip(route, route[1:]))
        for route in permutations(l))
)

def exo1(data: list[str]) -> int:
    loc, dist = parse_input(data)
    return solver(min, dist, loc)

def exo2(data: list[str]|str) -> Any:
    loc, dist = parse_input(data)
    return solver(max, dist, loc)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 605,
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
            'expected': 982,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)