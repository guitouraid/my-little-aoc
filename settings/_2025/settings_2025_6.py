from __future__ import annotations
from functools import reduce
import operator
import re
from typing import Iterable

READ_MODE = "nostrip"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_6.txt"

RE_OP = re.compile(r'([+*]) +')

class Operation:
    operations = {
        '+': sum,
        '*': lambda l: reduce(operator.mul, l)
    }

    def __init__(self, operator: str, operands: Iterable[int]):
        self.operator = operator
        self.operands = operands

    @classmethod
    def from_data_1(cls, data: tuple[str]) -> Operation:
        return cls(data[-1], map(int, data[:-1]))

    def operate(self) -> int:
        return self.operations[self.operator](self.operands)


def parse_input_1(data: str) -> Iterable[tuple[str]]:
    return zip(*[line.split() for line in data.strip('\n').split('\n')])

def parse_input_2(data: str):
    def to_numbers(lines: list[str]) -> Iterable[int]:
        for i in range(len(lines[0])):
            if n := ''.join([l[i] for l in lines]).replace(' ', ''):
                yield int(n)

    lines = data.strip('\n').split('\n')
    ops = lines[-1]
    lines = lines[:-1]
    for m in RE_OP.finditer(ops):
        yield Operation(m.group(1), to_numbers(list(map(lambda s: s[::-1], map(lambda l: l[m.start():m.end()][::-1], lines)))))

def exo1(data: str) -> int:
    operations = map(Operation.from_data_1, parse_input_1(data))
    return sum(map(lambda o: o.operate(), operations))

def exo2(data: str) -> int:
    operations = parse_input_2(data)
    return sum(map(lambda o: o.operate(), operations))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 4277556,
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
            'expected': 3263827,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)