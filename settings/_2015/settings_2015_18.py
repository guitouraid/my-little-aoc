from itertools import combinations_with_replacement, permutations
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_18_1.txt"

COMBOS = set(
    perm
    for combo in combinations_with_replacement((-1, 0, 1), 2)
    for perm in permutations(combo)
) - {(0,0)}

class Grid:
    def __init__(self, data: list[str], stuck: bool=False):
        self.data = data
        if stuck:
            self.data[0] = '#' + self.data[0][1:-1] + '#'
            self.data[-1] = '#' + self.data[-1][1:-1] + '#'
        self.rows = len(self.data)
        self.cols = len(self.data[0])
    
    def neighbours(self, r: int, c: int) -> list[str]:
        l = []
        for rel in COMBOS:
            rr = r+rel[0]
            cc = c+rel[1]
            if 0 <= rr < self.rows and 0 <= cc < self.cols:
                l.append(self.data[rr][cc])
            else:
                l.append('.') # off
        return l

    def next_state(self, l, c) -> str:
        n = self.neighbours(l,c)
        match self.data[l][c]:
            case '.': # off
                if n.count('#') == 3:
                    return '#'
                return '.'
            case '#': # on
                if n.count('#') in (2,3):
                    return '#'
                return '.'
            case _:
                raise ValueError(f'Unexpected ligth status: {self.data[l][c]}')

    def next_step(self) -> list[str]:
        l = []
        for r in range(self.rows):
            s = ''
            for c in range(self.cols):
                s += self.next_state(r,c)
            l.append(s)
        return l

    def count_on(self) -> int:
        return sum(l.count('#') for l in self.data)

def exo1(data: str, steps: int) -> int:
    grid = Grid([l for l in data.split('\n') if l])
    for i in range(steps):
        grid = Grid(grid.next_step())
    return grid.count_on()


def exo2(data: str, steps: int) -> int:
    grid = Grid([l for l in data.split('\n') if l], True)
    for i in range(steps):
        grid = Grid(grid.next_step(), True)
    return grid.count_on()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 4,
            'kw_args': {'steps': 4}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
            'kw_args': {'steps': 100}
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 17,
            'kw_args': {'steps': 5}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
            'kw_args': {'steps': 100}
        },
        'runner': exo2,
    },
)