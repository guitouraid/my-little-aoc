from collections import defaultdict
from itertools import count

import z3


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_10.txt"

class Machinery:
    def __init__(self, line: str) -> None:
        lights, *buttons, joltages = map(lambda f: f[1:-1], line.split())
        self.lights = sum(1 << i for i, c in enumerate(lights) if c == '#')
        self.buttons = [sum(1 << int(n) for n in b.split(',')) for b in buttons]
        self.joltages = list(map(int, joltages.split(',')))
        self.int_buttons = [list(map(int, b.split(','))) for b in buttons]

    def solve1(self) -> int:
        visited = {0}
        for cpt in count():
            if self.lights in visited:
                return cpt
            visited = {
                lights ^ trigger
                for lights in visited
                for trigger in self.buttons
            }
        raise ValueError('Might nevere happen, but pleases type checking')

    def solve2(self) -> int:
        solver = z3.Optimize()
        triggers = z3.IntVector("triggers", len(self.int_buttons))
        trig_idx = defaultdict(list)
        for i, b in enumerate(self.int_buttons):
            solver.add(triggers[i] >= 0)
            for j in b:
                trig_idx[j].append(i)
        for i, idx in trig_idx.items():
            solver.add(self.joltages[i] == sum(triggers[i] for i in idx))
        presses = z3.Sum(triggers)
        solver.minimize(presses)
        solver.check()
        return solver.model().eval(presses).as_long()


def exo1(data: list[str]) -> int:
    return sum(Machinery(line).solve1() for line in data)

def exo2(data: list[str]) -> int:
    return sum(Machinery(line).solve2() for line in data)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 7,
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
            'expected': 33,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)