from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

INPUT = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_16_1.txt"

def parse_input() -> dict:
    return {
        (spl := line.split(': '))[0]: int(spl[1])
        for line in INPUT.split('\n') if line
    }

def parse_data(data: list[str]) -> dict:
    return {
        int((spe := line.split(': ',1))[0].split()[1]): {
            (spi := v.split(': '))[0]: int(spi[1])
            for v in spe[1].split(', ')
        }
        for line in data
    }

def check_subset(cmp: dict, sue:dict) -> bool:
    def condition(prop: str) -> callable:
        match prop:
            case 'cats'|'trees':
                return lambda c, s: s[prop] > c[prop]
            case 'pomeranians'|'goldfish':
                return lambda c, s: s[prop] < c[prop]
            case _:
                return lambda c, s: s[prop] == c[prop]
    return all(condition(prop)(cmp, sue) for prop in sue.keys())

def exo1(data: list[str]) -> int:
    compare = parse_input().items()
    sues = parse_data(data)
    for sue, props in sues.items():
        if props.items() <= compare:
            return sue

def exo2(data: list[str]) -> int:
    compare = parse_input()
    sues = parse_data(data)
    for sue, props in sues.items():
        if check_subset(compare, props):
            return sue

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 0,
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
            'expected': 0,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)