import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_14_1.txt"

RE_NUMS = re.compile(r'\d+')

def readline(data: str) -> tuple[int,int,int]:
    return tuple(map(int, RE_NUMS.findall(data)))

def distance(rein: tuple[int,int,int], secs: int):
    speed, run, rest = rein
    rounds, remain = divmod(secs, run+rest)
    return speed * (rounds*run + min(run, remain))

# FINISH=1000
FINISH=2503

def exo1(data: list[str]) -> int:
    return max(distance(readline(line), FINISH) for line in data)

def exo2(data: list[str]) -> int:
    reins = [readline(line) for line in data]
    scores = [0 for _ in range(len(reins))]
    for sec in range(FINISH):
        current_scores = [distance(rein, sec+1) for rein in reins]
        top = max(current_scores)
        for i, score in enumerate(current_scores):
            scores[i] += score == top
    return max(scores)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 1120,
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
            'expected': 689,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)