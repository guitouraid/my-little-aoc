from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_1 = """
(())
()()
(((
(()(()(
))(((((
())
))(
)))
)())())
"""

TEST_DATA_2 = """
(()(())))
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_1_1.txt"



def exo1(data: str) -> Any:
    pcl = pop = 0
    for chr in data:
        match chr:
            case '(':
                pop += 1
            case ')':
                pcl += 1
    return pop-pcl


def exo2(data: str) -> Any:
    floor = 0
    step = 0
    for chr in data:
        match chr:
            case '(':
                floor += 1
                step +=1
            case ')':
                floor -= 1
                step += 1
                if floor < 0:
                    return step
    return step


settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 1,
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
            'expected': 9,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)