import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_1 = """
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
"""

TEST_DATA_2 = """
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_5_1.txt"

RE_TWICE_ANY = re.compile(r'.*(.)\1.*')
RE_VOWEL = re.compile(r'[aeiou]')
RE_BAD = re.compile(r'.*(ab|cd|pq|xy).*')

RE_TWICE_PAIR = re.compile(r'.*(.{2}).*\1.*')
RE_TWICE_ONE = re.compile(r'.*(.).\1.*')

def is_nice(line: str) -> bool:
    return bool(RE_TWICE_ANY.match(line)) and len(RE_VOWEL.findall(line)) >= 3 and not RE_BAD.match(line)

def is_nicer(line: str) -> bool:
    return bool(RE_TWICE_ONE.match(line) and RE_TWICE_PAIR.match(line))

def exo1(data: list[str]) -> int:
    return sum([is_nice(line) for line in data])

def exo2(data: list[str]|str) -> Any:
    return sum([is_nicer(line) for line in data])

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
            'from': TEST_DATA_2,
            'expected': 2,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)