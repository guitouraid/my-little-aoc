import re
from typing import Any

from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

TEST_DATA_2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2024_3_1.txt"

RE_MUL = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
RE_ALL = re.compile(r"(mul|do|don't)\(((\d{1,3}),(\d{1,3}))?\)")

def exo1(data: list[str]|str) -> Any:
    return sum([int(l)*int(r) for l, r in RE_MUL.findall(data.strip())])


def exo2(data: list[str]|str) -> Any:
    do = True
    ops = []
    for matching in RE_ALL.findall(data.strip()):
        match matching[0]:
            case 'mul':
                if do:
                    ops.append(int(matching[2])*int(matching[3]))
            case 'do':
                do = True
            case "don't":
                do = False
            case _:
                raise ValueError(f"Invalid operation: {matching[0]}")
    return sum(ops)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 161,
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