import hashlib
from itertools import count as icount
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = "abcdef"

REAL_DATA_2 = REAL_DATA_1 = "bgvyzdsv"

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_4_1.txt"

def exo(data: str, zc: int) -> int:
    zeroes = '0'*zc
    for i in icount():
        if str(hashlib.md5(f'{data}{i}'.encode()).hexdigest()).startswith(zeroes):
            return i

def exo1(data: str) -> Any:
    return exo(data, 5)

def exo2(data: list[str]|str) -> Any:
    return exo(data, 6)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 609043,
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