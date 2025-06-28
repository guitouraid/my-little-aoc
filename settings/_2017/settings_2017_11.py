from collections import Counter
from functools import cache


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
ne,ne,ne
ne,ne,sw,sw
ne,ne,s,s
se,sw,se,sw,sw
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_11.txt"


DIRS = ('n', 'ne', 'se', 's', 'sw', 'nw')
DIRS_LEN = len(DIRS)
DIST_DIRS = DIRS[:DIRS_LEN//2]
OPPOSITE = {v: DIRS[(k + 3) % DIRS_LEN] for k, v in enumerate(list(DIRS))}
CHECK_DS = {v: DIRS[(k + 2) % DIRS_LEN] for k, v in enumerate(list(DIRS))}
SET_DS = {v: DIRS[(k + 1) % DIRS_LEN] for k, v in enumerate(list(DIRS))}


class HexDist:
    def __init__(self, path: list[str]) -> None:
        c = Counter(path)
        self.dict = {k: c[k] for k in DIRS}

    def _simplify(self) -> None:
        for dir in DIRS:
            mini, maxi = sorted((dir, OPPOSITE[dir]), key=lambda s: self.dict[s])
            self.dict[maxi] -= self.dict[mini]
            self.dict[mini] = 0
        for dir in DIRS:
            check = CHECK_DS[dir]
            m = min((self.dict[dir],self.dict[check]))
            self.dict[dir] -= m
            self.dict[check] -= m
            self.dict[SET_DS[dir]] += m

    def distance(self) -> int:
        self._simplify()
        return sum(abs(self.dict[d] - self.dict[OPPOSITE[d]]) for d in DIST_DIRS)


def exo1(data: list[str]) -> list[int]:
    results = []
    for line in data:
        results.append(HexDist(line.split(',')).distance())
    return results

def exo2(data: list[str]) -> list[int]:
    results = []
    for line in data:
        path = line.split(',')
        results.append(
            max(HexDist(path[:i]).distance() for i in range(1, len(path) + 1))
        )
    return results


settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': [3, 0, 2, 3],
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
            'expected': [3, 2, 2, 3],
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
