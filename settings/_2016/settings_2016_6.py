from typing import Counter


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_6.txt"

def exo1(data: list[str]) -> str:
    result = ''
    for i in range(len(data[0])):
        c = Counter(line[i] for line in data)
        result += c.most_common(1)[0][0]
    return result

def exo2(data: list[str]) -> str:
    result = ''
    for i in range(len(data[0])):
        c = Counter(line[i] for line in data)
        result += c.most_common()[-1][0]
    return result

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 'easter',
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
            'expected': 'advent',
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
