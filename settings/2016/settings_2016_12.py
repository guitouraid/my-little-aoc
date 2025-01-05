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

class Memory(list):
    def get_address(self, value: int):
        for i, v in enumerate(self):
            if self.__getitem__(i) == value:
                return i
        self.append(value)
        return len(self) - 1

class Computer:
    def __init__(self, data: list[str]) -> None:
        self.registry = { c: 0 for c in 'abcd'}
        self.memory = Memory()
        self.program = []
        for line in data:
            self._read_instruction(line)

    def _cpy_mem(self, offset: int, reg: str, mem: int) -> int:
        self.registry[reg] = self.memory[mem]
        return offset + 1

    def _cpy_reg(self, offset: int, to_reg: str, from_reg: str) -> int:
        self.registry[to_reg] = self.registry[from_reg]
        return offset + 1

    def _inc(self, offset: int, reg: str) -> int:
        self.registry[reg] += 1
        return offset + 1

    def _dec(self, offset: int, reg: str) -> int:
        self.registry[reg] -= 1
        return offset + 1

    def _jnz_mem(self, offset: int, tst: int, by: int) -> int:
        if self.memory[tst] == 0:
            return offset + 1
        return offset + self.memory[by]

    def _jnz_reg(self, offset: int, tst: str, by: int) -> int:
        if self.registry[tst] == 0:
            return offset + 1
        return offset + self.memory[by]

    def _read_instruction(self, line: str) -> None:
        instr, *args = line.split()
        match instr:
            case 'cpy':
                if args[0] in self.registry:
                    self.program.append((self._cpy_reg, args[1], args[0]))
                else:
                    self.program.append((self._cpy_mem, args[1], self.memory.get_address(int(args[0]))))
            case 'inc':
                self.program.append((self._inc, args[0]))
            case 'dec':
                self.program.append((self._dec, args[0]))
            case 'jnz':
                if args[0] in self.registry:
                    self.program.append((self._jnz_reg, args[0], self.memory.get_address(int(args[1]))))
                else:
                    self.program.append((self._jnz_mem, self.memory.get_address(int(args[0])), self.memory.get_address(int(args[1]))))

    def run(self):
        offset = 0
        while 0 <= offset < len(self.program):
            instr, *args = self.program[offset]
            offset = instr(offset, *args)

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
