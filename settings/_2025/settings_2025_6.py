from functools import reduce
import operator


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_6.txt"

class Operation:
    operations = {
        '+': sum,
        '*': lambda l: reduce(operator.mul, l)
    }
    def __init__(self, data: tuple[str]):
        self.operator = data[-1]
        self.operands = map(int, data[:-1])

    def operate(self) -> int:
        return self.operations[self.operator](self.operands)

def parse_input(data: list[str]) -> list[str]:
    return list(zip(*[line.split() for line in data]))

def exo1(data: list[str]) -> int:
    operations = list(map(Operation, parse_input(data)))
    return sum(map(lambda o: o.operate(), operations))

def exo2(data: list[str]) -> int:
    return 0

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
            'expected': 0,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)