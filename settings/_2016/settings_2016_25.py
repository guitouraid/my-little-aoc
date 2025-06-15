from itertools import count
import re
from typing import LiteralString
from settings._2016.settings_2016_12 import Assembly, BaseComputer, Computer, ComputerState, Instruction
from settings._2016.settings_2016_23 import InstrPatternMatcher, MulHook, OptimizedComputer, ReHook, TglAssembly


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_25.txt"


class DivMod2Hook(ReHook):
    _IPM = InstrPatternMatcher(ComputerState.patterns([
        'cpy 2 {twoz}',
        'jnz {opmod2} 2',
        'jnz 1 6',
        'dec {opmod2}',
        'dec {twoz}',
        'jnz {twoz} -4',
        'inc {div2}',
        'jnz 1 -7',
        'cpy 2 {opmod2}',
        'jnz {twoz} 2',
        'jnz 1 4',
        'dec {opmod2}',
        'dec {twoz}',
        'jnz 1 -4'
    ]))
    _ARGS = ['twoz', 'opmod2', 'div2']
    _FS = "add {div2} (div {opmod2} 2) // cpy {opmod2} (mod {opmod2} 2) // clr {twoz} // j {offset}"

    def run(self, reg: dict[str,int]) -> int:
        ddest = self.arg_map['div2']
        mdest = self.arg_map['opmod2']
        twoz = self.arg_map['twoz']
        reg[ddest], reg[mdest] = divmod(reg[mdest], 2)
        reg[twoz] = 0
        return self._IPM.jump


class Out(Instruction):
    def _operate(self, comp: BaseComputer) -> int:
        comp.out.append(str(self.value(comp.cs.reg, self.args[0]))) # type: ignore
        return self._INC


class OutAssembly(Assembly):
    def __init__(self) -> None:
        super().__init__()
        self.language['out'] = Out


class PatternGenerator(OptimizedComputer):
    def __init__(self, data: list[str], asm: Assembly = OutAssembly(), dbg: bool = False, hooks: set[type[ReHook]] = {DivMod2Hook, MulHook}) -> None:
        super().__init__(data, asm=asm, dbg=dbg, hooks=hooks)
        self.out: list[str] = []

    def reset(self, **kw_args):
        self.cs.reset(**kw_args)
        self.out = []

    @property
    def output(self) -> str:
        return ''.join(self.out)

    def run(self):
        self.logger.debug(';;; run til out')
        super().run()
        self.logger.debug(f';;; output: {self.output}')
    

def exo1(data: list[str]) -> int:
    expected: LiteralString = '01'*7
    elen = len(expected)
    pf = PatternGenerator(data)
    for test in count():
        pf.logger.debug(f';;; iteration: {test}')
        pf.reset(reg={'a': test})
        while expected.startswith(pattern := pf.output) and pattern != expected:
            pf.run()
        if pattern == expected:
            return test
        elif test == 1000000:
            break
    raise ValueError('Infinite loop ?')


def exo2(data: list[str]) -> int:
    return 0

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
