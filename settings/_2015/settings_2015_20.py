import itertools


READ_MODE = "all"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
130
"""

### store file under `DATA_DIR`
REAL_DATA_2 = REAL_DATA_1 = """
36000000
"""

def visitors(idx: int) -> set[int]:
    return {i for i in itertools.chain.from_iterable((j, idx//j) for j in range(1, 1+int(idx**0.5)) if idx%j == 0)}

def visitors2(idx: int, limit:int):
    return filter(lambda x: idx <= x * limit, visitors(idx))
    

def exo1(data: str) -> int:
    goal = int(data)
    i = 1
    while 10*sum(visitors(i)) < goal:
        i += 1
    return i


def exo2(data: str, limit: int) -> int:
    goal = int(data)
    i = 1
    while 11*sum(visitors2(i, limit)) < goal:
        i += 1
    return i

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 8,
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
            'expected': 8,
            'kw_args': {'limit': 3}
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
            'kw_args': {'limit': 50}
        },
        'runner': exo2,
    },
)
