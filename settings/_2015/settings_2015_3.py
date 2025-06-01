from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
>
^>v<
^v^v^v^v^v
"""

TEST_DATA_2 = """
^v
^>v<
^v^v^v^v^v
"""
### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_3_1.txt"

def read_data(data: str) -> str:
    return ''.join(filter(lambda c: c in ('>', 'v', '<', '^'), data))

def visited(data: str) -> set[tuple[int,int]]:
    pos = (0,0)
    memo = {pos}
    for chr in data:
        match chr:
            case '>':
                pos = (pos[0], pos[1]+1)
            case 'v':
                pos = (pos[0]-1, pos[1])
            case '<':
                pos = (pos[0], pos[1]-1)
            case '^':
                pos = (pos[0]+1, pos[1])
            case '_':
                raise ValueError(f"Invalid char: {chr}")
        memo.add(pos)
    return memo

def with_robot(data: str) -> set[tuple[int,int]]:
    pos = [(0,0), (0, 0)]
    memo = {pos[0]}
    for i, chr in enumerate(data):
        ipos = i%2
        match chr:
            case '>':
                pos[ipos] = (pos[ipos][0], pos[ipos][1]+1)
            case 'v':
                pos[ipos] = (pos[ipos][0]-1, pos[ipos][1])
            case '<':
                pos[ipos] = (pos[ipos][0], pos[ipos][1]-1)
            case '^':
                pos[ipos] = (pos[ipos][0]+1, pos[ipos][1])
            case '_':
                raise ValueError(f"Invalid char: {chr}")
        memo.add(pos[ipos])
    return memo


def exo1(data: str) -> Any:
    return len(visited(read_data(data)))

def exo2(data: str) -> Any:
    return len(with_robot(read_data(data)))

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
            'from': REAL_FILE_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 14,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)