from typing import Callable


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_12.txt"

class IllegalInstruction(ValueError):
    pass

class Computer:
    def __init__(self, data: list[str]) -> None:
        self.registry = { c: 0 for c in 'abcd'}
        self.program = []
        for line in data:
            self._read_instruction(line)

    def _cpy(self, offset: int, value: str, reg: str) -> int:
        try:
            self.registry[reg] = self.registry.get(value) or int(value)
        except:
            raise IllegalInstruction(f'Could not process: copy({value}, {reg})')
        return offset + 1

    def _inc(self, offset: int, reg: str) -> int:
        self.registry[reg] += 1
        return offset + 1

    def _dec(self, offset: int, reg: str) -> int:
        self.registry[reg] -= 1
        return offset + 1

    def _jnz(self, offset: int, test: str, decal: str) -> int:
        # ambiguity about jnz specs
        # let us assume both test and decal coulb be int data or registry
        try:
            test_val = self.registry.get(test) or int(test)
            dec_val = self.registry.get(decal) or int(decal)
        except:
            raise IllegalInstruction(f'Could not process: jnz({test}, {decal})')
        if test_val == 0:
            return offset + 1
        return offset + dec_val

    def _read_instruction(self, line: str) -> None:
        instr, *args = line.split()
        self.program.append([instr, *args])

    def _real_cmd(self, cmd: str) -> Callable:
        try:
            return self.__getattribute__(f'_{cmd}')
        except AttributeError:
            raise IllegalInstruction(f'No such command: {cmd}')

    def run(self):
        offset = 0
        while 0 <= offset < len(self.program):
            instr, *args = self.program[offset]
            offset = self._real_cmd(instr)(offset, *args)

def exo1(data: list[str]) -> int:
    comp = Computer(data)
    comp.run()
    return comp.registry['a']

def exo2(data: list[str]) -> int:
    comp = Computer(data)
    comp.registry['c'] = 1
    comp.run()
    return comp.registry['a']

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 42,
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
            'expected': 42,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
