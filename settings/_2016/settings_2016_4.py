from collections import Counter
import re


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_4.txt"

RE_ROOM = re.compile(r'(.*)-(\d+)\[(.*)\]')

def parse_input(data: list[str]):
    return ((g[0], int(g[1]), g[2]) for g in map(lambda s: RE_ROOM.match(s).groups(), data) if g) # type: ignore

def check_room(room: str, code: int, checksum: str):
    c = Counter(room.replace('-', ''))
    if ''.join([kk for kk, vv in sorted(c.items(), key=lambda item: (-item[1], item[0]))]).startswith(checksum):
        return code
    return 0

def decrypt(room: str, code: int) -> str:
    start = ord('a')
    clear = ''
    for c in room:
        if c == '-':
            clear += ' '
        else:
            clear += chr((ord(c)-start+code)%26+start)
    return clear

def exo1(data: list[str]) -> int:
    return sum(check_room(*t) for t in parse_input(data))

def exo2(data: list[str]) -> int:
    for room, code, checksum in parse_input(data):
        if check_room(room, code, checksum):
            if decrypt(room, code) == 'northpole object storage':
                return code
    return 0

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 1514,
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
            'expected': 0,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
