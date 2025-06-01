import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Self, Union

from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2024_6_1.txt"

Rotator = Enum(
    value = 'Rotator',
    names = [
        ('^', 0),
        ('>', 1),
        ('v', 2),
        ('<', 3),
    ],
)
Rotator.rotate = lambda inst: Rotator((inst.value+1)%4)

class MemPos(set[tuple[int, int]]):
    def  __init__(self, orig: tuple[int, int]) -> None:
        self.orig = orig

    def __len__(self) -> int:
        return 1 + super().__len__()

    def __in__(self, item: tuple[int, int]) -> bool:
        return item == self.orig or super().__in__(item)

    def add(self, item: tuple[int, int]):
        if item != self.orig:
            super().add(item)


class GuardPos(tuple[tuple[int,int], Rotator]):
    @property
    def pos(self) -> tuple[int,int]:
        return self.__getitem__(0)

    @property
    def line(self) -> int:
        return self.__getitem__(0).__getitem__(0)

    @property
    def index(self) -> int:
        return self.__getitem__(0).__getitem__(1)

    @property
    def dir(self) -> Rotator:
        return self.__getitem__(1)

    def next_dir(self) -> Self:
        return GuardPos((self.pos, self.dir.rotate()))

    def next_pos(self) -> Self:
        line = self.line
        index = self.index
        match self.dir.value:
            case 0:
                line -= 1
            case 1:
                index += 1
            case 2:
                line += 1
            case 3:
                index -= 1
        return GuardPos(((line, index), self.dir))


class MemoDirPos(set[GuardPos]):
    pass


class Map:
    def __init__(self, map_data: list[str]) -> None:
        self.map = []
        self.guard = None
        for i, line in enumerate(map_data):
            for j, idx in enumerate(line):
                match line[j]:
                    case '.'|'#':
                        pass
                    case '^'|'v'|'<'|'>':
                        self.guard = GuardPos(((i,j), Rotator[line[j]]))
                        # line = line[:j] + '.' + line[j+1:]
                    case _:
                        raise ValueError(f'Unexpected value: {line[j]}')
            self.map.append(line)
        self.lines = len(self.map)
        self.cols = len(self.map[0])

    def inbounds(self, guard: Optional[GuardPos] = None) -> bool:
        (line, idx) = (guard or self.guard).pos
        return line >= 0 and idx >= 0 and line < self.lines and idx < self.cols

    def check_next_pos(self) -> Optional[GuardPos]:
        pos = self.guard.next_pos()
        if self.inbounds(pos):
            return pos
        return None

    def journey(self) -> MemPos:
        memo = MemPos(self.guard.pos)
        while self.inbounds():
            memo.add(self.guard.pos)
            check_pos = self.check_next_pos()
            if not check_pos:
                break
            if self.map[check_pos.line][check_pos.index] == '#':
                self.guard = self.guard.next_dir()
            else:
                self.guard = check_pos
        return memo

    def loop(self) -> bool:
        memo = MemoDirPos()
        while True:
            if self.guard in memo:
                return True
            memo.add(self.guard)
            check_pos = self.check_next_pos()
            if not check_pos:
                return False
            if self.map[check_pos.line][check_pos.index] == '#':
                self.guard = self.guard.next_dir()
            else:
                self.guard = check_pos
        # return False


class MapCheater:
    def __init__(self, map: Map) -> None:
        self.ini = map

    def cheat(self, line: int, idx: int) -> Map:
        new_map = []
        for i in range(self.ini.lines):
            nl = self.ini.map[i]
            if i == line:
                new_map.append(nl[:idx] + '#' + nl[idx+1:])
            else:
                new_map.append(nl)
        return Map(new_map)

    def try_all(self) -> int:
        return sum([self.cheat(line, idx).loop() for line, idx in self.ini.journey()])

def exo1(data: list[str]|str) -> Any:
    return len(Map(data).journey())

def exo2(data: list[str]|str) -> Any:
    # << 1926
    return MapCheater(Map(data)).try_all()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 41,
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
            'expected': 6,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)