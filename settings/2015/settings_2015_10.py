import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = REAL_DATA_2 = REAL_DATA_1 = "3113322113"

RE_DIGITS = re.compile(r'(1+|2+|3+|4+|5+|6+|7+|8+|9+|0+)')

nexti = lambda s: f"{len(s)}{s[0]}"

def transform(line: str) -> str:
    return ''.join(map(nexti, RE_DIGITS.findall(line)))

def repeat(line: str, times: int) -> str:
    for _ in range(times):
        line = transform(line)
    return line

def exo1(data: str) -> int:
    return len(repeat(data, 40))

def exo2(data: list[str]|str) -> Any:
    return len(repeat(data, 50))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 0,
        },
        'real_data': {
            'type': 'raw',
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
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)