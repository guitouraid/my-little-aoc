from curses.ascii import isdigit
import hashlib


READ_MODE = "all"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
abc
"""

### store file under `DATA_DIR`
REAL_DATA_2 = REAL_DATA_1 = """
ugkcyxxp
"""

class CodeMaker:
    def __init__(self, root: str) -> None:
        self.root = root
        self.len = 8

    def code(self) -> str:
        digits = ''
        suffix = 0
        while len(digits) < self.len:
            md5 = hashlib.md5(f'{self.root}{suffix}'.encode()).hexdigest()
            if md5.startswith('00000'):
                digits += md5[5]
            suffix += 1
        return digits

    def improved_code(self) -> str:
        digits = [None for i in range(self.len)]
        suffix = 0
        while not all(digits):
            md5 = hashlib.md5(f'{self.root}{suffix}'.encode()).hexdigest()
            if md5.startswith('00000'):
                try:
                    offset = int(md5[5])
                    if offset < self.len and not digits[offset]:
                        digits[offset] = md5[6] # type: ignore
                except:
                    pass
            suffix += 1
        return ''.join(digits) # type: ignore


def exo1(data: str) -> str:
    return CodeMaker(data).code()

def exo2(data: str) -> str:
    return CodeMaker(data).improved_code()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': '18f47a30',
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
            'expected': '05ace8e3',
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
