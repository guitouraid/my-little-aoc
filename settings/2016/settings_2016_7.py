import re


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_1 = """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""

TEST_DATA_2 = """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_7.txt"

RE_BR = re.compile(r'\[.*?\]')
# this one does not work as expected, apparently character class just do not support backref
# RE_TLS = re.compile(r'.*(.)([^\1])\2\1.*')
RE_TLS = re.compile(r'.*(\w)(?!\1)(\w)\2\1.*')
RE_SSL = re.compile(r'(\w)(?!\1)(\w)\1')

def is_tls(line: str) -> bool:
    for s in RE_BR.findall(line):
        if RE_TLS.match(s[1:-1]):
            return False
    for s in RE_BR.split(line):
        if RE_TLS.match(s):
            return True
    return False

def is_ssl(line: str) -> bool:
    brs = RE_BR.findall(line)
    for s in RE_BR.split(line):
        pos = 0
        while m := RE_SSL.search(s, pos):
            a, b = m.groups()
            rev = f'{b}{a}{b}'
            if any(rev in br for br in brs):
                return True
            pos = m.start() + 1
    return False

def exo1(data: list[str]) -> int:
    return sum(is_tls(line) for line in data)

def exo2(data: list[str]) -> int:
    return sum(is_ssl(line) for line in data)

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
            'from': REAL_FILE_1,
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
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
