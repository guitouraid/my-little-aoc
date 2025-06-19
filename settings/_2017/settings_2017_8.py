import re


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_8.txt"

class Interpreter:
    _RE_INSTR = re.compile(r'(\w+) (inc|dec) (-?\d+) if (\w+) (<|>|<=|>=|==|!=) (-?\d+)')
    _COND = {
        '<': lambda r, v: r < v,
        '>': lambda r, v: r > v,
        '<=': lambda r, v: r <= v,
        '>=': lambda r, v: r >= v,
        '==': lambda r, v: r == v,
        '!=': lambda r, v: r != v,
    }

    _INC_DEC = {
        'inc': lambda v: v,
        'dec': lambda v: -v,
    }

    def __init__(self) -> None:
        self.registry: dict[str,int] = {}

    def _check_reg(self, reg: str) -> None:
        if reg not in self.registry:
            self.registry[reg] = 0

    def _test_cond(self, reg: str, cmp: str, val: int) -> bool:
        self._check_reg(reg)
        return self._COND[cmp](self.registry[reg], val)

    def _operate(self, reg: str, ope: str, val: int) -> None:
        self._check_reg(reg)
        self.registry[reg] += self._INC_DEC[ope](val)

    def run_instr(self, instr: str) -> None:
        if not (m := self._RE_INSTR.match(instr)):
            raise ValueError(f'Invalid instruction: {instr}')
        if self._test_cond(m.group(4), m.group(5), int(m.group(6))):
            self._operate(m.group(1), m.group(2), int(m.group(3)))

    def run_program(self, pgm: list[str]) -> None:
        for line in pgm:
            self.run_instr(line)

def exo1(data: list[str]) -> int:
    interpreter = Interpreter()
    interpreter.run_program(data)
    return max(v for v in interpreter.registry.values())

def exo2(data: list[str]) -> int:
    maxi = 0
    interpreter = Interpreter()
    for line in data:
        interpreter.run_instr(line)
        maxi = max(maxi, *(v for v in interpreter.registry.values()))
    return maxi

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
            'from': REAL_DATA_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 10,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
