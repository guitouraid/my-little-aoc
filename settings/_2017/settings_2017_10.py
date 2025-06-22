

from collections import deque
from functools import reduce
from itertools import islice
from operator import xor


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
3,4,1,5
"""

TEST_DATA_2 = """
AoC 2017
1,2,3
1,2,4
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
230,1,2,221,97,252,168,169,57,99,0,254,181,255,235,167
"""

# def print_list(prefix: str, sample: list[int], current: int, long: int):
#     line = ''
#     for i, num in enumerate(sample):
#         if i ==  current:
#             line += f' ([{num}]'
#         elif i == (current + long - 1)%len(sample):
#             line += f' {num})'
#         else:
#             line += f' {num}'
#     print(f'{prefix}: {line}')
    
# def print_qr(prefix: str, qr: list[int]):
#     print(f'{prefix}: {" ".join(map(str, qr))}')

def transform(trans: list[int], length: int, rounds: int=1) -> list[int]:
    sample = list(range(length))
    current = 0
    skip = 0
    for _ in range(rounds):
        for long in trans:
            # print_list('\nbefore', sample, current, long)
            qr = sample[current:]+sample
            # print_qr('before', qr[:long])
            # print_qr('after', list(reversed((qr[:long]))))
            for i in range(long):
                sample[(current+i)%length] = qr[long-i-1]
            current = (current + long + skip) % length
            skip += 1
            # print_list('after', sample, current, long)
    return sample

def dense(hash: list[int]) -> str:
    compact = ''
    for i in range(0,256, 16):
        compact += f'{reduce(xor, hash[i:i+16]):02x}'
    return compact


def exo1(data: str, length: int) -> int:
    hash = transform([int(i) for i in data.split(',')], length)
    return hash[0]*hash[1]

def exo2(data: list[str]) -> list[str]:
    results = []
    for line in data:
        trans= [ord(c) for c in line] + [17, 31, 73, 47, 23]
        hash = transform(trans, 256, 64)
        results.append(dense(hash))
    return results

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 12,
            'kw_args': {'length': 5}
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_1,
            'kw_args': {'length': 256}
        },
        'runner': exo1,
    },
    {
        'read_mode': 'lines',
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': ['33efeb34ea91902bb2f59c9920caa6cd', '3efbe78a8d82f29979031a4aa0b16a9d', '63960835bcdc130f0b66d7ff4f6a5a8e'],
            # 'kw_args': {'length': 5}
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
            # 'kw_args': {'length': 255}
        },
        'runner': exo2,
    },
)
