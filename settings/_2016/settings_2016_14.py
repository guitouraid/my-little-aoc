from functools import lru_cache
from hashlib import md5
from itertools import count
import re


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
abc
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
ngcjuoqr
"""

RE_THREE = re.compile(r".*?(.)\1{2}.*")

def hash(chain: str) -> str:
    return md5(chain.encode()).hexdigest()

@lru_cache(None)
def xhash(salt: str, num: int, times: int = 0) -> str:
    ret = hash(f"{salt}{num}")
    for _ in range(times):
        ret = hash(ret)
    return ret

def has_three(chain: str) -> str|None:
    if m := RE_THREE.match(chain):
        return m.group(1)
    return None

@lru_cache
def has_five(chain: str, char: str) -> bool:
    return bool(re.match(rf".*{char}{{5}}.*", chain))

def sixtyfourth(data: str, stretch: int = 0) -> int:
    salt = data.strip()
    found = 0
    for i in count():
        code = xhash(salt, i, stretch)
        if got_three := has_three(code):
            for j in range(1, 1001):
                if has_five(xhash(salt, i+j, stretch), got_three):
                    found += 1
                    break
            if found == 64:
                return i
    raise ValueError('Supposedly unreachable code')


def exo1(data: str) -> int:
    return sixtyfourth(data)

def exo2(data: str) -> int:
    return sixtyfourth(data, 2016)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 22728,
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
            'expected': 0,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
