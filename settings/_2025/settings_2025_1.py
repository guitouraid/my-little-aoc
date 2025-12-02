READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_1.txt"

class Dial:
    mod = 100
    operate = {
        'L': lambda x: x - 1,
        'R': lambda x: x + 1
    }
    def __init__(self):
        self.cursor = 50
        self.zeroes = 0

    def read_instruction(self, data: str) -> int:
        try:
            offset = int(data[1:])
        except:
            raise ValueError(f'Not an int ? {data[1:]}')
        for i in range(offset):
            self.cursor = self.operate[data[0]](self.cursor) % self.mod
            self.zeroes += self.cursor == 0
        return self.cursor


class Dialer:
    def __init__(self, data: list[str]):
        self.dial = Dial()
        self.instructions = data

    def follow_cursor(self) -> list[int]:
        history = [(self.dial.cursor, 0)]
        for instruction in self.instructions:
            history.append(self.dial.read_instruction(instruction))
        return history


def exo1(data: list[str]) -> int:
    d = Dialer(data)
    numbers = d.follow_cursor()
    return sum([number == 0 for number in numbers])

# << 6294
def exo2(data: list[str]) -> int:
    d = Dialer(data)
    d.follow_cursor()
    return d.dial.zeroes

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 3,
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
            'expected': 6,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)