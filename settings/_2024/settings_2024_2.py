from typing import Any
from aoc import BaseData, ReadMode

###
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_1 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

# store file in `data` dir
REAL_FILE_1 = "2024_2_1.txt"

def read_data(data: list[str]) -> list[list[int]]:
    result = []
    for line in data:
        result.append([int(s) for s in line.split(' ')])
    return result

def is_valid(report: list[int]) -> bool:
    mul = 1
    if report[0] > report[1]:
        mul = -1
    for i in range(len(report)-1):
        if not 1 <= (report[i+1]-report[i])*mul <= 3:
            return False
    return True

def is_quite_valid(report: list[int]) -> bool:
    if is_valid(report):
        return True
    offsets = range(len(report))
    for i in offsets:
        if is_valid(report[:i]+report[i+1:]):
            return True
    return False

def exo1(data: list[str]) -> Any:
    reports = read_data(data)
    return sum([1 for report in reports if is_valid(report)])

def exo2(data: list[str]) -> Any:
    reports = read_data(data)
    return sum([1 for report in reports if is_quite_valid(report)])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 2,
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
            'from': TEST_DATA_1,
            'expected': 4,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
        },
        'runner': exo2,
    },
)