import re
from typing import Self
from settings._2016.settings_2016_12 import Computer, IllegalInstruction


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_23.txt"

class ExtendedComputer(Computer):
    def __init__(self, data: list[str]) -> None:
        super().__init__(data)

    def _tgl(self, offest: int, decal: str):
        target = offest + self.registry[decal] or int(decal)
        if target < len(self.program):
            instr, *args = self.program[target]
            if len(args) == 2:
                if instr == 'jnz':
                    new = 'cpy'
                else:
                    new = 'jnz'
            elif instr == 'inc':
                new = 'dec'
            else:
                new = 'inc'
            self.program[target][0] = new
        return offest + 1

    def run(self):
        offset = 0
        while 0 <= offset < len(self.program):
            instr, *args = self.program[offset]
            try:
                offset = self._real_cmd(instr)(offset, *args)
            except IllegalInstruction:
                offset += 1


# kamoulox
class ReMulHook:
    _RE_MULT = re.compile(r'inc ([a-d]),dec ([a-d]),jnz \2 -2,dec ([a-d]),jnz \3 -5')
    _ARGS = ['dest', 'op1', 'op2']
    _FS = "add {dest} (mul {op1} {op2}) // clr {op1} {op2} // j {offset}"
    _JUMP = 5

    def __init__(self, rmatch: re.Match) -> None:
        self.arg_map = {k: v for k, v in zip(self._ARGS, rmatch.groups())}

    def as_str(self) -> str:
        return self._FS.format(offset=self._JUMP, **self.arg_map)

    def run(self, reg: dict[str,int]) -> int:
        dest= self.arg_map['dest']
        op1 = self.arg_map['op1']
        op2 = self.arg_map['op2']
        reg[dest] += reg[op1] * reg[op2]
        reg[op1] = reg[op2] = 0
        return self._JUMP

    @classmethod
    def try_me(cls, program: list[str], pc: int, reg: dict[str,int]) -> Self|None:
        if pc + cls._JUMP - 1 >= len(program):
            return None
        if not (rm := cls._RE_MULT.match(','.join(program[pc:pc+cls._JUMP]))):
            return None
        if len(rm.groups()) > len(set(rm.groups())):
            return None
        # should probably also test for zero values in registers, even took the arg! But NO
        return cls(rm)


class Optimizer:
    @classmethod
    def try_hook(cls, program: list[list[str]], pc: int, reg: dict[str,int]) -> tuple[int,str]|None:
        adapted = [ ' '.join(cmd) for cmd in program ]
        if optim := ReMulHook.try_me(adapted, pc, reg):
            return(optim.run(reg), optim.as_str())
        return None


class OptimizedComputer(ExtendedComputer):
    def __init__(self, data: list[str]) -> None:
        super().__init__(data)
        self.pc = 0

    def _state(self, hook: str|None = None, end: bool = False) -> str:
        if hook:
            return f'{self.pc}\t{hook}\t; hooked: {self.program[self.pc]}\treg: {self.registry}'
        if end:
            return f'{self.pc}\tEnd of program\t;reg: {self.registry}'
        return f'{self.pc}\t{self.program[self.pc]}\t;reg: {self.registry}'
   
    def run(self):
        while 0 <= self.pc < len(self.program):
            if hook := Optimizer.try_hook(self.program, self.pc, self.registry):
                print(self._state(hook=(hook[1])))
                self.pc += hook[0]
            else:
                print(self._state())
                instr, *args = self.program[self.pc]
                try:
                    self.pc = self._real_cmd(instr)(self.pc, *args)
                except IllegalInstruction:
                    self.pc += 1
        print(self._state(end=True))

def exo1(data: list[str]) -> int:
    comp = ExtendedComputer(data)
    comp.registry['a'] = 7
    comp.run()
    return comp.registry['a']

def exo2(data: list[str]) -> int:
    comp = OptimizedComputer(data)
    comp.registry['a'] = 12
    comp.run()
    return comp.registry['a']

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 3,
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
