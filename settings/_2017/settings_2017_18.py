from collections import defaultdict, deque
from enum import Enum


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_18.txt"


class Prog:
    def __init__(self) -> None:
        self.registry: defaultdict[str, int] = defaultdict(int)
        self.pc = 0

    def get_value(self, arg: str) -> int:
        try:
            return int(arg)
        except:
            return self.registry[arg]


class Duet(Prog):
    def __init__(self, data: list[str]) -> None:
        self.program: list[str] = data
        self.sound = -1

    def _process_instruction(self, line: str) -> bool:
        instr, *args = line.split()
        match instr:
            case 'snd':
                self.sound = self.get_value(args[0])
                self.pc += 1
                return False
            case 'set':
                self.registry[args[0]] = self.get_value(args[1])
                self.pc += 1
                return False
            case 'add':
                self.registry[args[0]] += self.get_value(args[1])
                self.pc += 1
                return False
            case 'mul':
                self.registry[args[0]] *= self.get_value(args[1])
                self.pc += 1
                return False
            case 'mod':
                self.registry[args[0]] %= self.get_value(args[1])
                self.pc += 1
                return False
            case 'rcv':
                if self.get_value(args[0]) != 0:
                    return True
                self.pc += 1
                return False
            case 'jgz':
                if self.get_value(args[0]) > 0:
                    self.pc += self.get_value(args[1])
                else:
                    self.pc += 1
                return False
            case _:
                raise ValueError(f'Invalid instruction: {instr}')
     
    def run(self) -> int:
        while 0 <= self.pc < len(self.program):
            if self._process_instruction(self.program[self.pc]):
                return self.sound
        raise ValueError('Exit without return')

class Duettist(Prog):
    def __init__(self, pnum: int) -> None:
        super().__init__()
        self.registry['p'] = pnum
        self.rcv: deque[int] = deque([])
        self.waiting = False
        self.sent = 0

    def receive(self, val: int) -> None:
        self.rcv.append(val)
        self.waiting = False

class Duettists:
    def __init__(self, data: list[str]) -> None:
        self.instructions: list[str] = data
        self.progs: list[Duettist] = [Duettist(i) for i in range(2)]
        self.pg = 0
        self.len = len(self.instructions)

    def _process_instruction(self, pg: int, line: str):
        instr, *args = line.split()
        current = self.progs[pg]
        other = self.progs[1-pg]
        match instr:
            case 'snd':
                other.receive(current.get_value(args[0]))
                current.pc += 1
                current.sent += 1
            case 'set':
                current.registry[args[0]] = current.get_value(args[1])
                current.pc += 1
            case 'add':
                current.registry[args[0]] += current.get_value(args[1])
                current.pc += 1
            case 'mul':
                current.registry[args[0]] *= current.get_value(args[1])
                current.pc += 1
            case 'mod':
                current.registry[args[0]] %= current.get_value(args[1])
                current.pc += 1
            case 'rcv':
                if current.rcv:
                    current.registry[args[0]] = current.rcv.popleft()
                    current.pc += 1
                else:
                    current.waiting = True
                    self.pg = 1 - self.pg
            case 'jgz':
                if current.get_value(args[0]) > 0:
                    current.pc += current.get_value(args[1])
                else:
                    current.pc += 1
            case _:
                raise ValueError(f'Invalid instruction: {instr}')

    def run(self) -> int:
        while any(0<= p.pc < self.len and not p.waiting for p in self.progs):
            self._process_instruction(self.pg, self.instructions[self.progs[self.pg].pc])
        return self.progs[1].sent

def exo1(data: list[str]) -> int:
    return Duet(data).run()

def exo2(data: list[str]) -> int:
    return Duettists(data).run()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 4,
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
            'expected': 1,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
