READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
65
8921
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_15.txt"

class Generator:
    COEF = [16807, 48271]
    DIV = 2147483647
    SIXTEEN = pow(2, 16)

    def __init__(self, offset: int, seed: int) -> None:
        self.coef = self.COEF[offset]
        self.current = seed

    def next(self):
        self.current = (self.current * self.coef) % self.DIV

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Generator):
            return self.current & 0xFFFF == other.current & 0xFFFF
        return False


class TrickyGen(Generator):
    CHECK = [4, 8]

    def __init__(self, offset: int, seed: int) -> None:
        super().__init__(offset, seed)
        self.check = self.CHECK[offset]

    def next(self):
        while True:
            super().next()
            if self.current % self.check == 0:
                break


def parse_line(line: str) -> int:
    return int(line.split()[-1])

def exo1(data: list[str]) -> int:
    assert len(data) == 2
    gens = [Generator(i, n) for i, n in enumerate(map(parse_line, data))]
    s = 0
    for _ in range(40000000):
        gens[0].next()
        gens[1].next()
        s += gens[0] == gens[1]
    return s

def exo2(data: list[str]) -> int:
    assert len(data) == 2
    gens = [TrickyGen(i, n) for i, n in enumerate(map(parse_line, data))]
    s = 0
    for _ in range(5000000):
        gens[0].next()
        gens[1].next()
        s += gens[0] == gens[1]
    return s

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 588,
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
            'expected': 309,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
