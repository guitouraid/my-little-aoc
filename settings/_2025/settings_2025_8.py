from __future__ import annotations
from functools import reduce
from itertools import combinations, count
from operator import mul
from typing import NamedTuple


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_8.txt"


class SpaceCoord(NamedTuple):
    x: int
    y: int
    z: int

    def square_distance(self, other: SpaceCoord) -> int:
        return pow(other.x - self.x, 2) + pow(other.y - self.y, 2) + pow(other.z - self.z, 2)

    @classmethod
    def from_data(cls, data: str) -> SpaceCoord:
        return cls(*map(int, data.split(',')))

class Junction:
    def __init__(self, data: list[str]) -> None:
        self.boxes = [SpaceCoord.from_data(line) for line in data]
        self.ordered_pairs = sorted(combinations(self.boxes, 2), key=lambda t: t[0].square_distance(t[1]))

    def _join(self, steps: int|None = None) -> tuple[list[int],tuple[SpaceCoord,SpaceCoord]]:
        groups: list[list[SpaceCoord]] = []
        length = len(self.boxes)

        def in_group(box: SpaceCoord) -> int|None:
            for i, g in enumerate(groups):
                if box in g:
                    return i
            return None

        for i in count():
            b1, b2 = self.ordered_pairs[i]
            g1 = in_group(b1)
            g2 = in_group(b2)
            match g1, g2:
                case None, None:
                    groups.append([b1, b2])
                case None, int():
                    groups[g2].append(b1)
                case int(), None:
                    groups[g1].append(b2)
                case _:
                    if g2 != g1:
                        groups[g1] += groups[g2]
                        groups.remove(groups[g2])
            if steps and i == steps -1:
                break
            elif len(groups) == 1 and len(groups[0]) == length:
                break
        return ([len(g) for g in groups], (b1, b2)) # pyright: ignore[reportPossiblyUnboundVariable]

    def join_steps(self, steps: int) -> list[int]:
        return sorted(self._join(steps)[0], reverse=True)

    def join_all(self) -> tuple[SpaceCoord,SpaceCoord]:
        return self._join()[1]

def exo1(data: list[str], steps: int) -> int:
    lengths = Junction(data).join_steps(steps)
    return reduce(mul, lengths[:3])

def exo2(data: list[str]) -> int:
    b1, b2 = Junction(data).join_all()
    return b1.x * b2.x

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 40,
            'kw_args': {'steps': 10},
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_1,
            'kw_args': {'steps': 1000},
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 25272,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)