import re
from typing import Any, Union
from aoc import ReadMode

### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_0 = "abcdefgh"
TEST_DATA_1 = "ghijklmn"
REAL_DATA = "cqjxjnds"

RE_TWD = re.compile(r'([a-z])\1.*([a-z])\2')

A_ORD = ord('a')

def prepare_chars():
    ret = { 'by_chr': {}, 'by_num': {}}
    for i in range(26):
        c = chr(i+A_ORD)
        ret['by_chr'] |= {c:i}
        ret['by_num'] |= {i:c}
    return ret

class Char(tuple[int,str]):
    mapping = prepare_chars()

    @classmethod
    def get(cls, input: Union[str,int]):
        if isinstance(input, int):
            try: return Char((input, cls.mapping['by_num'][input]))
            except KeyError: raise ValueError(f'Invalid input: {input}')
        elif isinstance(input, str):
            try: return Char((cls.mapping['by_chr'][input], input))
            except KeyError: raise ValueError(f'Invalid input: {input}')
        else:
            raise ValueError(f'Invalid input: {input}')

    @property
    def int(self) -> int:
        return self.__getitem__(0)

    @property
    def chr(self) -> str:
        return self.__getitem__(1)

    def inc(self):
        if self.chr == 'z':
            return (Char((0, 'a')), True)
        return (self.get(self.int+1), False)

class PasswordChanger:
    forbidden = 'ilo'

    def __init__(self, pwd: str):
        i = Char.get('i')
        self.chars = [Char.get(c) for c in pwd]

    @property
    def len(self):
        return len(self.chars)

    @property
    def str(self):
        return ''.join([c.chr for c in self.chars])

    @property
    def ints(self):
        return [c.int for c in self.chars]

    def _bypass(self, i: int):
        self.chars[i], _ = self.chars[i].inc()
        for j in range(i+1, self.len):
            self.chars[j] = Char.get(0)

    def _ini_bypass(self):
        for i in range(self.len):
            if self.chars[i].chr in self.forbidden:
                self._bypass(i)
                break

    def _inc_pass(self):
        carry = True
        for i in range(self.len-1, 0, -1):
            if carry:
                self.chars[i], carry = self.chars[i].inc()
                if self.chars[i].chr in self.forbidden:
                    self._bypass(i)
                    break
            else:
                break

    def _invalid(self) -> bool:
        return \
            not RE_TWD.search(self.str)\
            or  not any((a == b - 1 == c - 2 for a, b, c in zip(self.ints, self.ints[1:],self.ints[2:])))

    def validate_next(self) -> str:
        self._ini_bypass()
        next = self._inc_pass()
        while self._invalid():
            next = self._inc_pass()
        return self.str

def exo1(data: str) -> str:
    return PasswordChanger(data).validate_next()

def exo2(data: list[str]|str) -> Any:
    return PasswordChanger(PasswordChanger(data).validate_next()).validate_next()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            # 'from': TEST_DATA_0,
            # 'expected': "abcdffaa",
            'from': TEST_DATA_1,
            'expected': "ghjaabcc",
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
            'from': TEST_DATA_0,
            'expected': "abcdffaa",
            # 'from': TEST_DATA_1,
            # 'expected': "ghjaabcc",
            'expected': 0,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA,
        },
        'runner': exo2,
    },
)