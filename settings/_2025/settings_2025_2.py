from textwrap import wrap


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_2.txt"

class RangeChecker:
    def __init__(self, data: str):
        start, stop = data.split('-')
        self.range = range(int(start), int(stop) + 1)

    def check(self, deep: bool) -> int:
        if deep:
            return sum([self._deep_check(num) for num in self.range])
        return sum([self._check_number(num) for num in self.range])

    def _check_number(self, num: int) -> int:
        digits = str(num)
        if (length := len(digits)) & 1:
            return 0
        middle = length // 2
        return num if digits[:middle] == digits[middle:] else 0

    def _deep_check(self, num: int) -> int:
        digits = str(num)
        length = len(digits)
        for i in range(1, length // 2 + 1):
            if length % i:
                continue
            if len(set(wrap(digits, i))) == 1:
                return num
        return 0


class RangesChecker:
    def __init__(self, data: str):
        self.ranges = [RangeChecker(r) for r in data.split(',')]

    def check(self, deep: bool = False) -> int:
        return sum([r.check(deep) for r in self.ranges])

def exo1(data: str) -> int:
    return RangesChecker(data).check()

def exo2(data: str) -> int:
    return RangesChecker(data).check(True)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 1227775554,
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
            'expected': 4174379265,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)