import re


READ_MODE = "all"

### test/real data as raw string or file
TEST_DATA = """
To continue, please consult the code grid in the manual.  Enter the code at row 4, column 5.
"""

### store file under `DATA_DIR`
REAL_DATA = """
To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019.
"""

RE_NUM = re.compile(r'\d+')

def parse_input(data: str) -> list[int]:
    return [int(i) for i in RE_NUM.findall(data)]

def next_code(code: int) -> int:
    return (code * 252533) % 33554393

def solve_santa(row: int, col: int) -> int:
    code = 20151125
    rows = crow = ccol = 1
    while crow != row or ccol != col:
        if rows == ccol:
            rows += 1
            crow = rows
            ccol = 1
        else:
            ccol += 1
            crow -= 1
        code = next_code(code)
    return code

def exo1(data: str) -> int:
    row, col = parse_input(data)
    return solve_santa(row, col)

def exo2(data: list[str]) -> int:
    return 0

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA,
            'expected': 10600672,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA,
            'expected': 0,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA,
        },
        'runner': exo2,
    },
)
