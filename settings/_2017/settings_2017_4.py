from collections import Counter


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_1 = """
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
"""
TEST_DATA_2 = """
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_4.txt"

def transform(line: str):
    tr = []
    for word in line.split():
        tr.append(''.join(sorted(word)))
    return Counter(tr).values()

def exo1(data: list[str]) -> int:
    return sum(
        all(
            vv == 1  for vv in v
        )
        for v in map(lambda s: Counter(s.split()).values(), data)
    )

def exo2(data: list[str]) -> int:
    return sum(
        all(
            vv == 1 for vv in v
        )
        for v in map(transform, data)
    )

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 2,
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
            'expected': 3,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
