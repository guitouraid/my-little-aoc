from dataclasses import dataclass
from functools import cached_property
import re
from typing import Self


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""


### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_7.txt"


RP = re.compile(rf'(\w+) \((\d+)\)(?: -> (.*))?')

@dataclass
class Program:
    name: str
    weight: int
    sub: list[str]

    @classmethod
    def from_str(cls, line: str) -> Self:
        m = RP.match((line))
        if not m:
            raise ValueError(f'Invalid program ? {line}')
        l = []
        if sub :=m.group(3):
            l = [p.strip() for p in sub.split(',')]
        return cls(m.group(1), int(m.group(2)), l)


class Tower:
    def __init__(self, data: list[str]) -> None:
        self.data, self.root = self._build(data)

    @classmethod
    def _build(cls, data: list[str]) -> tuple[dict[str,Program],str]:
        d = {}
        roots = set()
        subs = set()
        for p in map(Program.from_str, data):
            d[p.name] = p
            for name in p.sub:
                if name in roots:
                    roots.remove(name)
                subs.add(name)
            if p.name not in subs:
                roots.add(p.name)
        return d, list(roots)[0]


class PiledTower:
    def __init__(self, tower: Tower, which: str) -> None:
        self.prog: Program = tower.data[which]
        self.children: tuple[PiledTower, ...] = tuple(PiledTower(tower, name) for name in self.prog.sub)
        self.by_weight: dict[int,list[PiledTower]] = {}
        for child in self.children:
            self.by_weight.setdefault(child.weight, []).append(child)
        self.by_weight

    @cached_property
    def children_weight(self) -> int:
        return sum(c.weight for c in self.children)

    @cached_property
    def weight(self) -> int:
        return self.prog.weight + self.children_weight

    @cached_property
    def sorted_weights(self):
        return sorted(self.by_weight.values(), key=len)

    def find_unbalanced(self, expected = 0) -> int:
        match len(self.by_weight):
            case 0 | 1:
                return expected - self.children_weight
            case 2:
                sc = self.sorted_weights
                return sc[0][0].find_unbalanced(sc[1][0].weight)
            case _:
                raise ValueError('Should never happen!')
        

def exo1(data: list[str]) -> str:
    t = Tower(data)
    return t.root

def exo2(data: list[str]) -> int:
    t = Tower(data)
    pt = PiledTower(t, t.root)
    return pt.find_unbalanced()

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 'tknk',
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
            'expected': 60,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
