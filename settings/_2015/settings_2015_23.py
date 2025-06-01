READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2015_23.txt"

class Computer:
    def __init__(self, data: list[str], a_start: int = 0) -> None:
        self.registers = {
            'a': a_start,
            'b': 0,
        }
        self.pointer = 0
        self.instructions = tuple(l.split(' ', 1) for l in data)
        self.end = len(self.instructions)
        self.conditionals = {
            'jio': lambda d: d == 1, # weird!
            'jie': lambda d: not d & 1
        }

    def process(self) -> int:
        while 0 <= self.pointer < self.end:
            instr, operands = self.instructions[self.pointer]
            match instr:
                case 'inc':
                    self.registers[operands] += 1
                    self.pointer += 1
                case 'hlf':
                    self.registers[operands] //= 2
                    self.pointer += 1
                case 'tpl':
                    self.registers[operands] *= 3
                    self.pointer += 1
                case 'jmp':
                    self.pointer += int(operands)
                case _:
                    register, offset = operands.split(', ')
                    if self.conditionals[instr](self.registers[register]):
                        self.pointer += int(offset)
                    else:
                        self.pointer +=1
        return self.registers['b']


def exo1(data: list[str]) -> int:
    return Computer(data).process()

def exo2(data: list[str]) -> int:
    return Computer(data, 1).process()

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
