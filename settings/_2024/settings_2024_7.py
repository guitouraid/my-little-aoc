from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2024_7_1.txt"

class Operators:
    @classmethod
    def from_data(cls, line: str):
        test, remain = line.split(':')
        numbers = [int(i) for i in remain.split(' ') if i]
        return Operators(int(test), numbers)

    def __init__(self, test: int, data: list[int]):
        self.test = test
        self.data = data

    def try_add(self, first: int, after: list[int], propagate: bool) -> int:
        return self.try_operators(first+after[0], after[1:], propagate)

    def try_mul(self, first: int, after: list[int], propagate: bool) -> int:
        return self.try_operators(first*after[0], after[1:], propagate)

    def try_concat(self, first: int, after: list[int]) -> int:
        return self.try_operators(int(str(first)+str(after[0])), after[1:], True)

    def try_operators(self, first: int, after: list[int], with_pipe: bool) -> int:
        if not after:
            if first == self.test:
                return first
            return 0
        elif first > self.test:
            return 0
        if with_pipe:
            return self.try_add(first, after, True) or self.try_mul(first, after, True) or self.try_concat(first, after)
        return self.try_add(first, after, False) or self.try_mul(first, after, False)

    def check(self, with_pipe: bool=False) -> int:
        return self.try_operators(self.data[0], self.data[1:], with_pipe)


# =882304362421
def exo1(data: list[str]) -> Any:
    return sum([Operators.from_data(line).check() for line in data])

# =?145149066755184
def exo2(data: list[str]) -> Any:
    return sum([Operators.from_data(line).check(True) for line in data])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 3749,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 11387,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)