from enum import Enum


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
.^^.^.^^^^
"""

### ... or file (store file under `DATA_DIR`)
REAL_DATA_2 = REAL_DATA_1 = """
^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.
"""

class SupportedChar(str, Enum):
    TRAP = '^'
    FREE = '.'


class Row(str):
    TRAP_PATTERNS = {'^^.', '.^^', '^..', '..^'}
    def _char__at(self, idx: int) -> str:
        if 0 <= idx < len(self):
            return self[idx]
        else:
            return SupportedChar.FREE.value

    def _get_pattern(self, idx: int) -> str:
        return ''.join(self._char__at(i) for i in range(idx-1, idx+2))

    def _next_char(self, idx: int) -> str:
        if self._get_pattern(idx) in self.TRAP_PATTERNS:
            return SupportedChar.TRAP
        return SupportedChar.FREE

    def next_row(self) -> str:
        next_l = [self._next_char(i) for i in range(len(self))]
        return ''.join(next_l)

class Tiles:
    def __init__(self, rows: int, start: Row) -> None:
        self.rows = rows
        self.start = start
        self.grid = [self.start]
        self._compute_rows()

    def _compute_rows(self) -> None:
        for i in range(self.rows-1):
            self.grid.append(Row(self.grid[i].next_row()))

    def count_free(self) -> int:
        return sum(row.count(SupportedChar.FREE.value) for row in self.grid)


def exo1(data: str, rows: int) -> int:
    return Tiles(rows, Row(data.strip())).count_free()

def exo2(data: str) -> int:
    return Tiles(400000, Row(data.strip())).count_free()


settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 38,
            'kw_args': {'rows': 10},
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_1,
            'kw_args': {'rows': 40},
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
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
