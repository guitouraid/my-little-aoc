

from functools import cache, reduce
from operator import mul


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_1 = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

TEST_DATA_2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_11.txt"


class Circuit:
    def __init__(self, data: list[str]) -> None:
        self.paths = {l[0][:-1]: l[1:] for l in map(lambda s: s.split(), data)}

    @cache
    def count_paths(self, start: str = 'you', end: str = 'out') -> int:
        if start == end:
            return 1
        return sum(self.count_paths(s, end) for s in self.paths.get(start, [])) # type: ignore

    def count_multi(self, steps: list[str]) -> int:
        return reduce(mul, map(lambda t: self.count_paths(*t), zip(steps, steps[1:]))) # type: ignore

def exo1(data: list[str]) -> int:
    return Circuit(data).count_paths() # type: ignore

def exo2(data: list[str]) -> int:
    return Circuit(data).count_multi(['svr', 'fft', 'dac', 'out'])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 5,
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
            'expected': 2,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)