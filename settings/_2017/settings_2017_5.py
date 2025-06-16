from typing import Callable


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
0
3
0
1
-3
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_5.txt"

def inc1(dec: int) -> int:
    return 1

def inc2(dec: int) -> int:
    if dec > 2:
        return -1
    return 1

def solve(maze: list[int], inc_method: Callable) -> int:
    steps = p = 0
    while 0 <= p < len(maze):
        dec = maze[p]
        maze[p] += inc_method(dec)
        p += dec
        steps += 1
    return steps

def exo1(data: list[str]) -> int:
    return solve([int(l) for l in data], inc1)

def exo2(data: list[str]) -> int:
    return solve([int(l) for l in data], inc2)

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
            'from': REAL_DATA_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 10,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
