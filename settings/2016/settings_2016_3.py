from itertools import islice


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_3.txt"

def batched(iterable, n):
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch

def parse_input(data: list[str]):
    return [tuple(map(int, line.split())) for line in data]

def ordered_input(data: list[str]):
    inverted = tuple(zip(*parse_input(data)))
    return [e for f in inverted for e in batched(f, 3)]

def is_valid(triangle: tuple[int, ...]):
    if len(triangle) != 3:
        raise ValueError(f'Invalid triangle: {triangle}')
    return all(triangle[i] < triangle[(i+1)%3] + triangle[(i+2)%3] for i in range(3))

def exo1(data: list[str]) -> int:
    return sum(is_valid(t) for t in parse_input(data))

def exo2(data: list[str]) -> int:
    return sum(is_valid(t) for t in ordered_input(data))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 0,
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
            'expected': 0,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
