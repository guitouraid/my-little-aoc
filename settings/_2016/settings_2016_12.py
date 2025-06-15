from collections.abc import Callable
import re
from typing import LiteralString


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


class MyLogger:
    def _no_dbg(self, input: str) -> None:
        pass

    def _dbg(self, input: str) -> None:
        print(input)

    def __init__(self, debug: bool) -> None:
        self.debug = self._dbg if debug else self._no_dbg


class IllegalInstruction(ValueError):
    pass

class BaseComputer:
    def __init__(self, data: list[str], dbg: bool=False) -> None:
        self.data = data
        self.logger = MyLogger(dbg)

class ComputerState:
    _R = 'abcd'
    _REG: dict[str, int] = { c: 0 for c in _R}
    _REP: LiteralString = rf"[{_R}]"
    _RR: re.Pattern[str] = re.compile(rf'.*? {{(\w+)}}.*?')

    def __init__(self) -> None:
        self.reg = self._REG
        self.pc = 0
        self.reset()

    def reset(self, clear: bool = True, reg: dict = {}, pc: int = 0) -> None:
        if clear:
            self.reg = self._REG
        self.reg |= reg
        self.pc = pc        

    def state(self):
        return f'\t;[pc]: {self.pc}\t[reg]: {self.reg}'

    @classmethod
    def patterns(cls, input: list[str]) -> list[str]:
        r: list[str] = []
        memo = {}
        for line in input:
            for m in cls._RR.findall(line):
                if m not in memo:
                    memo[m] = {
                        'f': True,
                        'v': {
                            True: f'(?P<{m}>{cls._REP})',
                            False: f'(?P={m})'
                        }
                    }
                else:
                    memo[m]['f'] = False
            r.append(line.format(**{k: v['v'][v['f']] for k, v in memo.items()}))
        return r


class Instruction:
    _INC = 1

    def __init__(self, instr: str|list[str]) -> None:
        if isinstance(instr, str):
            self.line = instr
            self.list = instr.split()
        else:
            self.list = instr
            self.line = ' '.join(instr)
        self.instr = self.list[0]
        self.args = self.list[1:]

    def _operate(self, comp: BaseComputer) -> int:
        raise NotImplementedError

    def _check_param(self, name: str, **kw_args):
        if name in kw_args:
            return kw_args[name]
        raise ValueError(f'Missing param: {name}')

    @classmethod
    def value(cls, registry: dict[str,int], input: str) -> int:
        if input in registry:
            return registry[input]
        return int(input)

    def operate(self, comp: BaseComputer) -> None:
        try:
            comp.cs.pc += self._operate(comp) # type: ignore
        except ValueError as e:
            raise IllegalInstruction(f'Could not process: {self.line} ({str(e)})')
   

class Cpy(Instruction):
    def _operate(self, comp: BaseComputer) -> int:
        comp.cs.reg[self.args[1]] = self.value(comp.cs.reg, self.args[0]) # type: ignore
        return self._INC

class Inc(Instruction):
    def _operate(self, comp: BaseComputer) -> int:
        comp.cs.reg[self.args[0]] += 1 # type: ignore
        return self._INC

class Dec(Instruction):
    def _operate(self, comp: BaseComputer) -> int:
        comp.cs.reg[self.args[0]] -= 1 # type: ignore
        return self._INC

class Jnz(Instruction):
    def _operate(self, comp: BaseComputer) -> int:
        if (test_val := self.value(comp.cs.reg, self.args[0])) == 0: # type: ignore
            return self._INC
        return self.value(comp.cs.reg, self.args[1]) # type: ignore


class Assembly:
    def __init__(self) -> None:
        self.language: dict[str, type[Instruction]] = {
            'cpy': Cpy,
            'inc': Inc,
            'dec': Dec,
            'jnz': Jnz,
        }

    def instruction(self, instr: str|list[str]) -> Instruction:
        for k, v in self.language.items():
            if (
                isinstance((instr), str) and\
                instr.startswith(f'{k} ')
            ) or instr[0] == k:
                return v(instr)
        raise IllegalInstruction(f"Unknown instruction: {instr}")

class Computer(BaseComputer):
    def __init__(self, data: list[str], asm: Assembly=Assembly(), dbg: bool=False) -> None:
        super().__init__(data,dbg)
        self.cs = ComputerState()
        self.asm = asm
        self.program = [asm.instruction(line) for line in data]

    def _state(self):
        return f'\t;[pc]: {self.cs.pc}\t[reg]: {self.cs.reg}'

    def run(self):
        while 0 <= self.cs.pc < len(self.program):
            self.logger.debug(self._state())
            instr = self.program[self.cs.pc]
            self.logger.debug(instr.line)
            instr.operate(self)
        self.logger.debug(f'{self._state()};\t(Stopped)')

def exo1(data: list[str]) -> int:
    comp = Computer(data)
    comp.run()
    return comp.cs.reg['a']

def exo2(data: list[str]) -> int:
    comp = Computer(data)
    comp.cs.reset(reg={'c': 1})
    comp.run()
    return comp.cs.reg['a']

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
