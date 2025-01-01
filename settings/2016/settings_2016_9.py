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

RE_REPEAT = re.compile(r'(.*?)\((\d+)x(\d+)\)(.*)')

def decoded_len(input: str, recurse=False):
    if m := RE_REPEAT.match(input):
        before, length, mult, after = m.groups()
        length = int(length)
        mult = int(mult)
        yield len(before)
        if recurse:
            yield from map(lambda x: x*mult,decoded_len(after[:length], recurse))
        else:
            yield len(after[:length]*mult)
        yield from decoded_len(after[length:], recurse)
    else:
        yield len(input)

def exo1(data: str) -> int:
    return sum(decoded_len(data))

def exo2(data: str) -> int:
    return sum(decoded_len(data, True))
    

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
