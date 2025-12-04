from itertools import product
from typing import NamedTuple


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_4.txt"

class Position(NamedTuple):
    x: int
    y: int


class RollStorage:
    moves = [
        (0, 1), (0, -1),
        (1, 1), (1, -1),
        (-1, 1), (-1, -1),
        (-1, 0), (1, 0),
    ]

    def __init__(self, data: list[str]):
        self.grid = data
        self.height = len(data)
        self.width = len(data[0])
        self.rolls = {
            pos for pos in map(
                lambda t: Position(t[0], t[1]),
                product(range(self.width), range(self.height))
            )
            if self.grid[pos.y][pos.x] == '@'
        }

    def _charat(self, pos: Position, rolls: set[Position]) -> str:
        return '@' if pos in rolls else '.'

    def _surrounding_rolls(self, pos: Position, rolls: set[Position]) -> set[Position]:
        return rolls & {
            p for p in map(
                lambda t: Position(pos.x + t[0], pos.y + t[1]),
                self.moves
            )
        }

    def _count_rolls_around(self, pos: Position, rolls: set[Position]) -> int:
        return len(self._surrounding_rolls(pos, rolls))

    def _reachable_rolls(self, rolls: set[Position]) -> set[Position]:
        return {
            pos for pos in rolls
            if self._count_rolls_around(pos, rolls) < 4
        }

    def count_reachable_rolls(self) -> int:
        return len(self._reachable_rolls(self.rolls))

    def count_removable_rolls(self) -> int:
        rolls = self.rolls.copy()
        while rem := self._reachable_rolls(rolls):
            rolls -= rem
        return len(self.rolls) - len(rolls)


def exo1(data: list[str]) -> int:
    return RollStorage(data).count_reachable_rolls()

def exo2(data: list[str]) -> int:
    return RollStorage(data).count_removable_rolls()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 13,
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
            'expected': 43,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)