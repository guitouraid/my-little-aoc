import re
from typing import Self
from settings._2016.settings_2016_12 import Assembly, BaseComputer, Computer, ComputerState, IllegalInstruction, Instruction


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


class Tgl(Instruction):
    def _operate(self, comp: BaseComputer) -> int:
        target: int = comp.cs.pc + Instruction.value(comp.cs.reg, self.args[0]) # type: ignore
        if 0 <= target < len(comp.program): # type: ignore
            i: Instruction = comp.program[target] # type: ignore
            if len(i.args) == 2:
                if i.instr == 'jnz':
                    new = 'cpy'
                else:
                    new = 'jnz'
            elif i.instr == 'inc':
                new = 'dec'
            else:
                new = 'inc'
            comp.program[target] = comp.asm.instruction([new] + i.args) # type: ignore
        return self._INC


class TglAssembly(Assembly):
    def __init__(self) -> None:
        super().__init__()
        self.language['tgl'] = Tgl


class ExtendedComputer(Computer):
    def __init__(self, data: list[str], asm: Assembly = TglAssembly(), dbg: bool = False) -> None:
        super().__init__(data, asm=asm, dbg=dbg)

    def run(self):
        while 0 <= self.cs.pc < len(self.program):
            self.logger.debug(self._state())
            instr = self.program[self.cs.pc]
            try:
                instr.operate(self)
                self.logger.debug(instr.line)
            except IllegalInstruction as ii:
                self.cs.pc += 1
                self.logger.debug(f'{instr.line}\t; ({str(ii)})')
        self.logger.debug(f'{self._state()}\t(Stopped)')


# kamoulox
class InstrPatternMatcher:
    def __init__(self, lines: list[str]) -> None:
        self.instructions = lines
        self.jump = len(lines)
        self._pattern = re.compile(r','.join(lines))

    def match(self, comp: Computer) -> None | re.Match[str]:
        if comp.cs.pc + self.jump  > len(comp.program):
            return None
        if not (ipm := self._pattern.match(','.join(i.line for i in comp.program[comp.cs.pc:comp.cs.pc+self.jump]))):
            return None
        if len(ipm.groups()) != len(set(ipm.groups())):
            return None
        # should probably also test for zero values in registers, even took the arg! But NO
        return ipm


class ReHook:
    _ARGS: list[str]
    _FS: str
    _IPM: InstrPatternMatcher

    def __init__(self, rmatch: re.Match) -> None:
        
        self.arg_map = {k: v for k, v in zip(self._ARGS, rmatch.groups())}

    def state(self) -> str:
        return self._FS.format(offset=self._IPM.jump, **self.arg_map)

    def run(self, reg: dict[str,int]) -> int:
        raise NotImplementedError

    @classmethod
    def try_me(cls, comp: Computer) -> Self|None:
        if m := cls._IPM.match(comp):
            return cls(m)
        return None


class MulHook(ReHook):
    _IPM = InstrPatternMatcher(ComputerState.patterns([
        'inc {dest}',
        'dec {op1}',
        'jnz {op1} -2',
        'dec {op2}',
        'jnz {op2} -5'
    ]))
    _ARGS = ['dest', 'op1', 'op2']
    _FS = "add {dest} (mul {op1} {op2}) // clr {op1} {op2} // j {offset}"

    def run(self, reg: dict[str,int]) -> int:
        dest= self.arg_map['dest']
        op1 = self.arg_map['op1']
        op2 = self.arg_map['op2']
        reg[dest] += reg[op1] * reg[op2]
        reg[op1] = reg[op2] = 0
        return self._IPM.jump


class Optimizer:
    def __init__(self, hooks: set[type[ReHook]]) -> None:
        self.hooks = hooks

    def try_hook(self, comp: Computer) -> tuple[int,str]|None:
        for hook in self.hooks:
            if optim := hook.try_me(comp):
                return(optim.run(comp.cs.reg), optim.state())
        return None


class OptimizedComputer(ExtendedComputer):
    def __init__(self, data: list[str], asm: Assembly = TglAssembly(), dbg: bool = False, hooks: set[type[ReHook]] = {MulHook}) -> None:
        super().__init__(data, asm=asm, dbg=dbg)
        self.optim = Optimizer(hooks)

    def run(self):
        while 0 <= self.cs.pc < len(self.program):
            self.logger.debug(self._state())
            i = self.program[self.cs.pc]
            if hook := self.optim.try_hook(self):
                self.logger.debug(f'{hook[1]}\t; hooked in: {i.line}')
                self.cs.pc += hook[0]
            else:
                self.logger.debug(i.line)
                try:
                    i.operate(self)
                    if i.instr == 'out':
                        # dirty to mention unknown instruction here, but does not harm
                        break
                except IllegalInstruction as ii:
                    self.cs.pc += 1
                    self.logger.debug(f'{i.line}\t; ({str(ii)})')
        self.logger.debug(f'{self._state()};\t({"Stopped"})')

def exo1(data: list[str]) -> int:
    comp = ExtendedComputer(data)
    comp.cs.reset(reg={'a': 7})
    comp.run()
    return comp.cs.reg['a']

def exo2(data: list[str]) -> int:
    comp = OptimizedComputer(data)
    comp.cs.reset(reg={'a': 12})
    comp.run()
    return comp.cs.reg['a']

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
            'expected': 3,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
