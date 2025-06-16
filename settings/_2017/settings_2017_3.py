from itertools import count, product
from typing import NamedTuple, Self


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
1024
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
289326
"""

class Position(NamedTuple):
    x: int
    y: int

    def add(self, other: Self) -> Self:
        return self._replace(x = self.x + other.x, y = self.y + other.y)

class Direction:
    DIRS = (Position(1,0), Position(0, 1), Position(-1, 0), Position(0, -1))

    def __init__(self) -> None:
        self._cursor = 0

    @property
    def current(self) -> Position:
        return self.DIRS[self._cursor]

    def rotate(self) -> None:
        self._cursor = (self._cursor + 1) % len(self.DIRS)

    @property
    def is_default(self) -> bool:
        return self._cursor == 0


class Grid:
    def __init__(self) -> None:
        self.current = self.start = Position(0,0)
        r = range(-1,2)
        self._close = [p for p in map( lambda t: Position(*t),product(r, r)) if p != self.start]
        self.pos: dict[Position,int] = {self.start: 1}
        self.dir = Direction()
        self.max = 0
        self._is_valid_pos = {
            self.dir.DIRS[0]: lambda p: p.x < self.max,
            self.dir.DIRS[1]: lambda p: p.y < self.max,
            self.dir.DIRS[2]: lambda p: -p.x < self.max,
            self.dir.DIRS[3]: lambda p: -p.y < self.max,
        }

    def fill(self, floor: int) -> int:
        while True:
            while next_pos := self.current.add(self.dir.current):
                if not self._is_valid_pos[self.dir.current](next_pos):
                    break
                sn = self._sum_neighbours(next_pos)
                if sn >= floor:
                    return sn
                self.pos[next_pos] = sn
                self.current = next_pos
            if self.dir.is_default:
                self.max += 1
                sn = self._sum_neighbours(next_pos)
                if sn >= floor:
                    return sn
                self.pos[next_pos] = sn
                self.current = next_pos
            self.dir.rotate()

    def _sum_neighbours(self, pos: Position) -> int:
        return sum(
            self.pos.get(pos.add(p), 0)
            for p in self._close
        )


def square_order_cap(number: int) -> tuple[int,int]:
    """min(n) verifying check <= square(1+2(n+1))"""
    for i in count():
        maxi = pow(1+ 2 * i, 2)
        if maxi >= number:
            return (i, maxi)
    raise ValueError('Should never happen)')

def diff_square(order: int) -> list[int]:
    l =[i for i in range(order+1)]
    return (l + l[::-1][1:-1])*4

def distance(number: int) -> int:
    order, cap = square_order_cap(number)
    perim = diff_square(order)
    return 2 * order - perim[cap - number]

# << 421
def exo1(data: str) -> int:
    return distance((int(data)))

def exo2(data: str) -> int:
    return Grid().fill(int(data))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 31,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 1968,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
