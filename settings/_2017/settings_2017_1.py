from collections import deque


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_1 = """
1122
1111
1234
91212129
"""
TEST_DATA_2 = """
1212
1221
123425
123123
12131415
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_1.txt"


def gotcha(number: str, offset= 1):
    decal = deque(number)
    for _ in range(offset):
        decal.append(decal.popleft())
    return sum(int(digit) for digit, after in zip(number, decal) if digit == after)


def exo1(data: list[str]) -> list[int]:
    results = []
    for number in data:
        results.append(gotcha(number))
    return results

def exo2(data: list[str]) -> list[int]:
    results = []
    for number in data:
        results.append(gotcha(number, len(number) // 2))
    return results

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': [3, 4, 0, 9],
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
            'expected': [6, 0, 4, 12, 4],
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
