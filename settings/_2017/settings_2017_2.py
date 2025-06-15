from itertools import combinations
import numbers


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_1 = """
5 1 9 5
7 5 3
2 4 6 8
"""
TEST_DATA_2 = """
5 9 2 8
9 4 7 3
3 8 6 5
"""
### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_2.txt"


def read_lines(data: list[str]):
    for line in data:
        yield [int(i) for i in line.split()]

def division(numbers: tuple[int,int]) -> int:
    mini = min(numbers)
    maxi = max(numbers)
    q, r = divmod(maxi, mini)
    if r:
        return 0
    return q

def find_div(numbers: list[int]) -> int:
    for pair in combinations(numbers, 2):
        if d := division(pair):
            return d
    return 0

def exo1(data: list[str]) -> int:
    return sum(max(numbers) - min(numbers) for numbers in read_lines(data))

def exo2(data: list[str]) -> int:
    return sum(find_div(numbers) for numbers in read_lines(data))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 18,
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
            'expected': 9,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
