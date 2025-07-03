from collections import deque

READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
3
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
345
"""



class Spinner:
    def __init__(self, spin: int) -> None:
        self.spin = spin
        self.lock = deque([0])
 
    def process(self, times: int):
        for i in range(1, times + 1):
            self.lock.rotate(-(self.spin + 1))
            self.lock.appendleft(i)

def exo1(data: str) -> int:
    s = Spinner(int(data))
    s.process(2017)
    return s.lock[1]

def exo2(data: str) -> int:
    s = Spinner(int(data))
    s.process(50000000)
    while s.lock[0] != 0:
        s.lock.append(s.lock.popleft())
    return s.lock[s.lock.index(0) + 1]

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 638,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 1222153,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
