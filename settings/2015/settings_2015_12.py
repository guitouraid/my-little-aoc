import json
import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_1 = """
[1,2,3]
{"a":2,"b":4}
[[[3]]]
{"a":{"b":4},"c":-1}
{"a":[-1,1]}
[-1,{"a":1}]
[]
{}
"""

TEST_DATA_2 = """
[[1,2,3],
[1,{"c":"red","b":2},3],
{"d":"red","e":[1,2,3,4],"f":5},
[1,"red",5]]
"""
### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_12_1.txt"

RE_NUM = re.compile(r'-?\d+')

def find_nums(jsn) -> int:
    if isinstance(jsn, dict):
        values = jsn.values()
        if "red" in values:
            return 0
        else:
            return sum([find_nums(value) for value in values])
    elif isinstance(jsn, list):
        return sum([find_nums(value) for value in jsn])
    elif isinstance(jsn, int):
        return jsn
    return 0

def exo1(data: list[str]|str) -> Any:
    return sum(map(int, RE_NUM.findall(data)))

# << 119433
def exo2(data: list[str]|str) -> Any:
    return sum([find_nums(json.loads(data))])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 18,
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
            'expected': 16,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)