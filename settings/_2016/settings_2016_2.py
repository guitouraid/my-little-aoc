import copy


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
ULL
RRDDD
LURDL
UUUUD
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_2.txt"

class Numpad:
    directions = {
        'U': {'axis': 'row', 'move': -1},
        'D': {'axis': 'row', 'move': 1},
        'L': {'axis': 'col', 'move': -1},
        'R': {'axis': 'col', 'move': 1},
    }

    def __init__(self, pad, row: int, col: int) -> None:
        self.pos = {'row': row, 'col': col}
        self.pad = pad
        self.MAX= len(pad)

    def _valid(self, coord: dict[str, int]) -> bool:
        return 0 <= coord['row'] < self.MAX and 0 <= coord['col'] < self.MAX and self.pad[coord['row']][coord['col']] is not None

    def single_move(self, direction: str) -> None:
        direct = self.directions[direction]
        next_pos = copy.deepcopy(self.pos)
        next_pos[direct['axis']] += direct['move'] # type: ignore
        if self._valid(next_pos):
            self.pos = next_pos

    def charat(self) -> str:
        return self.pad[self.pos['row']][self.pos['col']]

def exo1(data: list[str]) -> str:
    PAD = (
        ('1','2','3'),
        ('4','5','6'),
        ('7','8','9')
    )
    nums = []
    np = Numpad(PAD, 1, 1)
    for line in data:
        for c in line:
            np.single_move(c)
        nums.append(np.charat())
    return ''.join(nums)

def exo2(data: list[str]) -> int:
    PAD = (
        (None,None,'1', None, None),
        (None, '2','3','4', None),
        ('5', '6', '7','8','9'),
        (None, 'A','B','C', None),
        (None,None,'D', None, None),
    )
    nums = []
    np = Numpad(PAD, 2, 0)
    for line in data:
        for c in line:
            np.single_move(c)
        nums.append(np.charat())
    return ''.join(nums)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': "1985",
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
            'expected': '5DB3',
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
