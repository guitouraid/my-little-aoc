from functools import reduce
from settings._2016.settings_2016_15 import RE_NUMBERS


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""


class Connexions:
    def __init__(self, data: list[str]) -> None:
        self._parse_input(data)

    def find_prog(self, prog: str) -> set|None:
        for s in self.cnx:
            if prog in s:
                return s
        return None

    def _find_progs(self, progs: list[str]) -> set|None:
        found = []
        for s in self.cnx:
            if any(p in s for p in progs):
                found.append(s)
        if found:
            for f in found:
                self.cnx.remove(f)
            s = reduce(lambda s1, s2: s1|s2, found)
            self.cnx.append(s)
            return s
        return None

    def _parse_input(self, data: list[str]) -> None:
        self.cnx: list[set] = []
        for line in data:
            numbers = RE_NUMBERS.findall(line)
            if s:= self._find_progs(numbers):
                s |= set(numbers)
            else:
                self.cnx.append(set(numbers))


### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_12.txt"


def exo1(data: list[str]) -> int:
    if not (s := Connexions(data).find_prog(('0'))):
        raise ValueError('EXpected a zero somewhere!')
    return len(s)

def exo2(data: list[str]) -> int:
    return len(Connexions(data).cnx)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 6,
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
