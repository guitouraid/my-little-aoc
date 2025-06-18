from copy import copy
from itertools import count, cycle


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
0   2   7   0
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_6.txt"


class AwaLoop:
    def __init__(self, data: str) -> None:
        self.data = data
        self.current = self.start = [int(s) for s in data.split()]
        self.seen = [self.start]

    def _idx_of_max(self, numbers: list[int]):
        return max((i_n for i_n in enumerate(numbers)), key= lambda t: t[1])[0]

    def _dispatch(self, numbers: list[int], index: int) -> list[int]:
        ret = copy(numbers)
        ret[index] = 0
        loop = cycle(list(range(index + 1, len(numbers))) + list(range(0, index)) +[index])
        for i, _ in zip(loop, range(numbers[index])):
            ret[i] += 1
        return ret

    def find_loop(self) -> int:
        for i in count(1):
            self.current = self._dispatch(self.current, self._idx_of_max(self.current))
            if self.current in self.seen:
                return i
            self.seen.append(self.current)
        raise ValueError('Should never happen')

def exo1(data: str) -> int:
    return AwaLoop(data).find_loop()

def exo2(data: str) -> int:
    al = AwaLoop((data))
    al.find_loop()
    return len(al.seen) - al.seen.index(al.current)

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
            'expected': 4,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
