READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
10000
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
10111100110001111
"""


def dragon_curve(input: str) -> str:
    dest = { '0': '1', '1': '0'}
    inverted = ''.join(dest[c] for c in input[::-1])
    return f'{input}0{inverted}'

def checksum(input: str) -> str:
    dest = {
        '01': '0',
        '10': '0',
        '00': '1',
        '11': '1'
    }
    return ''.join(dest[c1+c2] for (c1, c2) in zip(input[::2], input[1::2]))



def exercise(seed: str, length: int) -> str:
    while len(seed) < length:
        seed = dragon_curve(seed)
    check = checksum(seed[:length])
    while len(check) % 2 == 0:
        check = checksum(check)
    return check

def exo1(data: str, length: int) -> str:
    return exercise(data.strip(), length)

def exo2(data: str, length: int) -> str:
    return exercise(data.strip(), length)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': "01100",
            'kw_args': {'length': 20}
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_1,
            'kw_args': {'length': 272}
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
            'type': 'raw',
            'from': REAL_DATA_2,
            'kw_args': {'length': 35651584}
        },
        'runner': exo2,
    },
)
