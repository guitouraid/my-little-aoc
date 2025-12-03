READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
987654321111111
811111111111119
234234234234278
818181911112111
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_3.txt"

class Bank:
    def __init__(self, data: str):
        self.batteries = data

    # def joltage(self) -> int:
    #     fi, fc = max([(i, c) for i, c in enumerate(self.batteries[:-1])], key=lambda t: (t[1], -t[0]))
    #     sc = max([c for c in self.batteries[fi+1:]])
    #     return int(fc+sc)

    def joltage(self, batteries: int) -> int:
        s = ''
        idx = 0
        for i in range(batteries - 1, -1, -1):
            subi, nc = max([t for t in enumerate(self.batteries[idx:-i if i else None])], key=lambda t: (t[1], -t[0]))
            s += nc
            idx += subi + 1
        return int(s)



class PowerBank:
    def __init__(self, data: list[str]):
        self.banks = [Bank(line) for line in data]

    def total_joltage(self, batteries: int =2) -> int:
        return sum([b.joltage(batteries) for b in self.banks])

def exo1(data: list[str]) -> int:
    return PowerBank(data).total_joltage()

def exo2(data: list[str]) -> int:
    return PowerBank(data).total_joltage(12)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 357,
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
            'expected': 3121910778619,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)