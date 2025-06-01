from dataclasses import dataclass
from hashlib import md5
from os import path
from typing import SupportsIndex


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
ihgpwlah
kglvqrro
ulqzkmiv
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
qtetzkpl
"""


@dataclass
class PosMove:
    x: int
    y: int
    move: str


class PMPath(list[PosMove]):
    def path_str(self) -> str:
        return ''.join(pos.move for pos in self)


class Vault:
    MAX = 3
    OPTIONS = [
        PosMove(0, -1, 'U'),
        PosMove(0, 1, 'D'),
        PosMove(-1, 0, 'L'),
        PosMove(1, 0, 'R'),
    ]

    def __init__(self, password: str, not_bigger: int|None = None) -> None:
        self.password = password
        self.not_bigger = not_bigger
        self.start = PosMove(0,0,'')

    def is_goal(self, pos: PosMove) -> bool:
        return pos.x == pos.y == self.MAX
    
    def next_pos(self, pos: PosMove, direction: PosMove) -> PosMove:
        return PosMove(pos.x+direction.x, pos.y+direction.y, direction.move)

    def is_valid(self, pos: PosMove, letter: str) -> bool:
        return  0 <= pos.x <= self.MAX and \
                0 <= pos.y <= self.MAX and \
                letter in 'bcdef'

    def next_moves(self, pos: PosMove, seed: str) -> list[PosMove]:
        moves = []
        for direction, letter in zip(self.OPTIONS, seed):
            if self.is_valid((move := self.next_pos(pos, direction)), letter):
                moves.append(move)
        return moves

    def _get_path(self, traverse: list[PMPath]):
        while len(traverse):
            current_path = traverse.pop(0)
            current_move = current_path[-1]
            as_str = current_path.path_str()
            if self.is_goal(current_move):
                yield as_str
                if not self.not_bigger or len(as_str) >= self.not_bigger:
                    break
                else:
                    continue
            checksum = md5((self.password+as_str).encode()).hexdigest()
            for next_move in self.next_moves(current_move, checksum):
                traverse.append(PMPath(current_path.copy()+[next_move]))

    def shortest_path(self) -> str:
        for path in self._get_path([PMPath([self.start])]):
            return path or 'No path from `_get_path` !'
        else:
            return 'No path from `shortest_path` !'
    
    def max_len(self) -> int:
        return max(
            (length := len(path) for path in self._get_path([PMPath([self.start])])),
            key=lambda pm_path: (length, path)
        )
        


def exo1(data: list[str]) -> list[str]:
    results = []
    for seed in [line.strip() for line in data]:
        results.append(Vault(seed).shortest_path())
    return results

def exo2(data: list[str]) -> list[str]:
    results = []
    for seed in [line.strip() for line in data]:
        results.append(Vault(seed, 1000).max_len())
    return results

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': ['DDRRRD', 'DDUDRLRRUDRD', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'],
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
            'expected': [370, 492, 830],
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
