import re


READ_MODE = "all"

### test/real data as raw string or file
TEST_DATA_1 = """
X(8x2)(3x3)ABCY
"""

TEST_DATA_2 = """
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_9.txt"

RE_REPEAT = re.compile(r'\((\d+)x(\d+)\)')

def decoded_len(input: str, recurse=False) -> int:
    if m := RE_REPEAT.search(input):
        length, mult = [int(x) for x in m.groups()]
        istart = m.start()
        tstart = m.end()
        tend = tstart+length
        if recurse:
            return len(input[:istart]) + decoded_len(input[tstart:tend]*mult, recurse) + decoded_len(input[tend:], recurse)
        else:
            return len(input[:istart]) + len(input[tstart:tend]*mult) + decoded_len(input[tend:])
    return len(input)

def exo1(data: str) -> int:
    return decoded_len(data)

def exo2(data: str) -> int:
    return decoded_len(data, True)
    

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
            'from': REAL_FILE_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 445,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
