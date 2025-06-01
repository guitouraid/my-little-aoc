from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_FILE_1 = "2015_8_1_TEST.txt"

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_8_1.txt"

def exo1(data: list[str]|str) -> Any:
    return sum(len(line) - len(eval(line)) for line in data)

def exo2(data: list[str]|str) -> Any:
    return sum([line.count('"') + line.count('\\') +2 for line in data])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'file',
            'from': TEST_FILE_1,
            'expected': 12,
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
            'type': 'file',
            'from': TEST_FILE_1,
            'expected': 19,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)