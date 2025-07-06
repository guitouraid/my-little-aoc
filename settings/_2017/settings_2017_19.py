
READ_MODE = "nostrip"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ \
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_19.txt"


class Network:
    def __init__(self, data: list[str]) -> None:
        self.map = {complex(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[0]))}
        self.current = self.start = complex(data[0].index('|'), 0)
        self.direction = complex(0, 1)

    def _turn(self) -> None:
        for turn in [0+1j, 0-1j]:
            next_dir = self.direction * turn
            next_pos = self.current + next_dir
            if (c := self.map.get(next_pos, ' ')) != ' ':
                self.current = next_pos
                self.direction = next_dir

    def transport(self) -> list[str]:
        word: list[str] = []
        while (sign := self.map[self.current]) != ' ':
            word.append(sign)
            if sign == '+':
                self._turn()
            else:
                self.current += self.direction
        return word
        return ''.join(c for c in word if c.isalpha())

def exo1(data: str) -> str:
    res = Network(data.split('\n')).transport()
    return ''.join(c for c in res if c.isalpha())

def exo2(data: str) -> int:
    res = Network(data.split('\n')).transport()
    return len(res)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 'ABCDEF',
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 38,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
