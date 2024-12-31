import re


READ_MODE = "all"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
R5, L5, R5, R3
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_1.txt"

RE_INST = re.compile(r'[RL]\d+')

def parse_input(data: str) -> list[tuple[str,int]]:
    return [(ins[0], int(ins[1:])) for ins in RE_INST.findall(data)]

class GridMover:
    directions = [
        {'axis': 'lat', 'mult': 1}, # N
        {'axis': 'long', 'mult': 1}, # E
        {'axis': 'lat', 'mult': -1}, # S
        {'axis': 'long', 'mult': -1}, # W
    ]

    turns = {
        'L': -1,
        'R': 1
    }

    def __init__(self, check_visisted: bool=False) -> None:
        self.dir = 0 # N
        self.pos = {'lat': 0, 'long': 0}
        self.check_visited = check_visisted
        self.memo = {self.position()}

    def position(self) -> tuple[int,int]:
        return self.pos['lat'], self.pos['long']

    def move(self, turn: str, dist: int) -> bool:
        self.dir = (self.dir + self.turns[turn]) % 4
        direct = self.directions[self.dir]
        if self.check_visited:
            for i in range(1, dist+1):
                self.pos[direct['axis']] += direct['mult'] # type: ignore
                pos = self.position()
                if pos in self.memo:
                    return True
                self.memo.add(pos)
        else:
            self.pos[direct['axis']] += dist * direct['mult'] # type: ignore
        return False

    def distance(self) -> int:
        return abs(self.pos['lat'])+abs(self.pos['long'])

def exo1(data: str) -> int:
    gm = GridMover()
    for t, i in parse_input(data):
        gm.move(t, i)
    return gm.distance()

# << 269
def exo2(data: str) -> int:
    gm = GridMover(True)
    for t, i in parse_input(data):
        if gm.move(t, i):
            break
    return gm.distance()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 12,
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
