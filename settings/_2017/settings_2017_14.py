from functools import reduce
from settings._2017.settings_2017_10 import dense, transform


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
flqrgnkx
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
vbqugkhl
"""

def hash(seed: str) -> str:
    # also need the traling numbers addition!
    return ''.join(f'{int(d, 16):04b}' for d in dense(hash=transform([ord(c) for c in seed] + [17, 31, 73, 47, 23], 256, 64)))

def hashes(data: str) -> list[str]:
    return [ hash(f'{data}-{i}') for i in range(128) ]

def adjacent_point(t: tuple[int,int], tt: tuple[int,int]):
    return abs(tt[0] - t[0]) + abs(tt[1] - t[1]) == 1

def adjacent_set(t: tuple[int,int], s: set[tuple[int,int]]) -> bool:
    return any(adjacent_point(t, tt) for tt in s)

def exo1(data: str) -> int:
    return sum(h.count('1') for h in hashes(data))

def exo2(data: str) -> int:
    h = hashes(data)
    adjacents: list[set] = []
    for i in range(128):
        for j in range(128):
            if h[i][j] == '1':
                t = (i,j)
                close: list[set] = []
                for s in adjacents:
                    if adjacent_set(t, s):
                        close.append(s)
                if close:
                    for s in close:
                        adjacents.remove(s)
                    s = reduce(lambda s1, s2: s1|s2, close) | {t}
                    adjacents.append(s)
                else:
                    adjacents.append({t})
    return len(adjacents)



settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 8108,
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
            'expected': 1242,
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
