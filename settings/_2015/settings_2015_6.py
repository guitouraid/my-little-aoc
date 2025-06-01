import re
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_1 = """
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
"""
TEST_DATA_2 = """
turn on 0,0 through 0,0
toggle 0,0 through 999,999
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_6_1.txt"

RE_INSTR = re.compile(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')

class Pos(tuple[int,int]):
    @property
    def abc(self) -> int:
        return self.__getitem__(0)

    @property
    def ord(self) -> int:
        return self.__getitem__(1)

class Instruction(tuple[str,Pos,Pos]):
    @property
    def name(self) -> str:
        return self.__getitem__(0)

    @property
    def start(self) -> Pos:
        return self.__getitem__(1)

    @property
    def end(self) -> Pos:
        return self.__getitem__(2)

    @classmethod
    def read(self, line: str) -> tuple[str,Pos,Pos]:
        matching = RE_INSTR.match(line)
        if not matching:
            raise ValueError(f"Invalid line: {line}")
        return Instruction((matching.group(1), Pos((int(matching.group(2)), int(matching.group(3)))), Pos((int(matching.group(4)), int(matching.group(5))))))

    def apply(self) -> tuple[str,range,range]:
        return (self.name, range(self.start.ord, self.end.ord+1), range(self.start.abc, self.end.abc+1))

class Map:
    lambdas = {
        False: {
            'turn on': lambda x: True,
            'turn off': lambda x: False,
            'toggle': lambda x: not x,
        },
        True: {
            'turn on': lambda x: x+1,
            'turn off': lambda x: max(0,x-1),
            'toggle': lambda x: x+2,
        },
    }

    def __init__(self, data):
        self.map = [[False for col in range(1000)] for row in range(1000)]
        self.instructions = list(map(Instruction.read, data))

    def run(self, improved: bool=False) -> int:
        for (instr, lr, cr) in [i.apply() for i in self.instructions]:
            fun = self.lambdas[improved][instr]
            for line in lr:
                for col in cr:
                    self.map[line][col] = fun(self.map[line][col])
        return sum([self.map[row][col] for col in range(1000) for row in range(1000)])

def exo1(data: list[str]) -> int:
    return Map(data).run()

def exo2(data: list[str]) -> int:
    return Map(data).run(True)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 998996,
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
            'expected': 2000001,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)