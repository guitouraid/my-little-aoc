from itertools import count
import math


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
0: 3
1: 2
4: 4
6: 4
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_13.txt"


class Scanner:
    def __init__(self, size: int) -> None:
        assert size > 0
        self.size = size

    def caught(self, tick: int) -> bool:
        return tick % ((self.size - 1) * 2) == 0

class Firewall:
    def __init__(self, data: list[str]) -> None:
        self.scanners = {int(k): Scanner(int(v)) for k, v in map(lambda s: s.split(': '), data)}
        self.size = max(self.scanners.keys()) + 1

    def caught(self, tick: int = 0) -> dict[int,Scanner]:
        return {k: s for k, s in self.scanners.items() if s.caught(tick + k)}

    def penalty(self, tick: int = 0) -> int:
        return sum(k * s.size for k, s in self.caught(tick).items())


def exo1(data: list[str]) -> int:
    return Firewall(data).penalty()

def exo2(data: list[str]) -> int:
    # quite slow but bearable
    f = Firewall(data)
    for i in range(math.lcm(*(s.size for s in f.scanners.values())) * f.size):
        if len(f.caught(i)) == 0:
            return i
    raise ValueError('Should never happen')

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 24,
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
            'expected': 10,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
