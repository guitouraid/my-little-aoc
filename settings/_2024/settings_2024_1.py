import re
from typing import Any
from aoc import BaseData, ReadMode

###
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

# store file in `data` dir
REAL_FILE = "2024_1.txt"

def read_data(data: list[str]) -> tuple[list[int], list[int]]:
    l_one = []
    l_two = []
    for line in data:
        one, two = re.split(r'\s+', line)
        l_one.append(int(one))
        l_two.append(int(two))
    return (l_one, l_two)

def exo1(data: list[str]) -> Any:
    l_one, l_two = read_data(data)
    l_one.sort()
    l_two.sort()
    return sum([abs(one-two) for one, two in zip(l_one, l_two)])

def accounts(data: list[int]) -> dict[int: int]:
    result = {}
    for i in data:
        result.setdefault(i, 0)
        result[i] += 1
    return result

def exo2(data: list[str]) -> Any:
    left, right = read_data(data)
    left = accounts(left)
    right = accounts(right)
    return sum([i*count*right.get(i, 0) for i, count in left.items()])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA,
            'expected': 11,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA,
            'expected': 31,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE,
        },
        'runner': exo2,
    },
)