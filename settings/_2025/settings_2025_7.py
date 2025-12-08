from typing import Iterable, NamedTuple


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_7.txt"

class Position(NamedTuple):
    x: int
    y: int


class Manifolder:
    def __init__(self, data: list[str]) -> None:
        self.grid = data
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def is_divider(self, pos: Position) -> bool:
        return self.grid[pos.y][pos.x] == '^'

    def divisions(self) -> Iterable[int]:
        beams = {self.grid[0].index('S')}
        for y in range(2, self.height, 2):
            splitters = [p for p in map(lambda x: Position(x, y), range(self.width)) if self.is_divider(p) and p.x in beams]
            beams |= {p.x-1 for p in splitters}
            beams |= {p.x+1 for p in splitters}
            beams -= {p.x for p in splitters}
            yield len(splitters)

    def timelines(self) -> int:
        timelines = { i: int(self.grid[0][i] == 'S') for i in range(self.width)}
        for y in range(2, self.height, 2):
            splitters = [p for p in map(lambda x: Position(x, y), range(self.width)) if self.is_divider(p) and p.x in timelines.keys()]
            for s in splitters:
                v = timelines[s.x]
                timelines[s.x] = 0
                timelines[s.x-1] += v
                timelines[s.x+1] += v
        return sum(timelines.values())

def exo1(data: list[str]) -> int:
    return sum(Manifolder(data).divisions())

def exo2(data: list[str]) -> int:
    return Manifolder(data).timelines()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 21,
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
            'expected': 40,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)