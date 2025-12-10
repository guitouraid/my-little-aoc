from __future__ import annotations

from itertools import combinations
from typing import NamedTuple
from shapely.geometry.polygon import Polygon

READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_9.txt"

class Position(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_data(cls, data: str) -> Position:
        return cls(*map(int, data.split(',')))
    
    def surface(self, other: Position) -> int:
        return (abs(other.x-self.x) + 1) * (abs(other.y-self.y) + 1)

def make_poly(t: tuple[Position,Position]) -> Polygon:
    xmin = min(t[0].x, t[1].x)
    xmax = max(t[0].x, t[1].x)
    ymin = min(t[0].y, t[1].y)
    ymax = max(t[0].y, t[1].y)
    return Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])

def exo1(data: list[str]) -> int:
    red = [Position.from_data(line) for line in data]
    return max(first.surface(second) for first, second in combinations(red, 2))

def exo2(data: list[str]) -> int:
    red = [Position.from_data(line) for line in data]
    shape = Polygon(red)
    return max(t[0].surface(t[1]) for t in combinations(red, 2) if shape.contains(make_poly(t)))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 50,
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
            'expected': 24,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)