from itertools import product
from typing import NamedTuple, Self as Self


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_22.txt"

class Position(NamedTuple):
    x: int
    y: int

class Node(NamedTuple):
    pos: Position
    size: int
    load: int

    def _assert(self):
        assert self.size >= self.load

    @classmethod
    def from_values(cls, pos: Position, size: int, load: int) -> Self:
        o = cls(pos, size, load)
        o._assert()
        return o

    @property
    def left(self) -> int:
        return self.size - self.load

    def can_fill(self, other: Self) -> bool:
        return self != other and self.load != 0 and self.load <= other.left

    def is_empty(self) -> bool:
        return self.load == 0


class NodesGrid(list[list[Node]]):
    pass


class Grid:
    def __init__(self, data: list[str]) -> None:
        last_node = data[-1].split()[0].split('-')
        self.height = 1 + int(last_node.pop()[1:])
        self.width = 1 + int(last_node.pop()[1:])
        self.nodes = NodesGrid()
        start = 0
        while not data[start].startswith('/'):
            start += 1
        nodes = data[start:][::-1]
        for x in range(self.width):
            current = []
            for y in range(self.height):
                line = nodes.pop().split()
                current.append(Node(
                    Position(x, y),
                    int(line[1][:-1]),
                    int(line[2][:-1])
                ))
            self.nodes.append(current)
        self.empty, self.available = self._find_avail()
        self.wall = self._find_wall()

    def _find_avail(self) -> tuple[Node,list[tuple[Node,Node]]]:
        empty = None
        pairs = []
        for node, other in product(self.all(), self.all()):
           if node.can_fill(other):
                pairs.append((node, other))
           elif node.is_empty():
               empty = node
        assert empty is not None
        return (empty, pairs)

    def _find_wall(self) -> Position:
        return [n.pos for n in self.all() if not n.can_fill(self.empty)][0]

    def is_wall(self, node: Node) -> bool:
        # dirty but enough for both test and real cse
        if node.pos.y == self.wall.y:
            if self.wall.x == 0:
                return node.pos.x == 0
            return node.pos.x >= self.wall.x
        return False

    def node_char(self, node: Node, avail: list[Node]|None=None) -> str:
        if avail:
            if node.is_empty():
                return '-'
            if node in avail:
                return '.'
            return '#'
        if node.pos.x == 0 and node.pos.y == 0:
            return '!'
        if node.pos.x == self.width -1 and node.pos.y == 0:
            return 'G'
        if self.is_wall(node):
            return '#'
        if node.is_empty():
            return '-'
        return '.'

    def nodes_str(self, avail: list[Node]|None=None):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                node = self.nodes[x][y]
                line.append(f'{self.node_char(node, avail)}')
            lines.append(''.join(line))
        return '\n'.join(lines)

    def as_str(self, avail=None) -> str:
        return f"Grid({self.width}X{self.height}) ->\tNodes:\n{self.nodes_str(avail)}\n"

    def all(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (self.nodes[x][y])

    def count_available_pairs(self) -> int:
        print(self.as_str())
        print(self.as_str(self.pairs_to_list()))
        return len(self.available)

    def shortest_path(self):
        X_MAX = self.width - 1
        reach_G = self.empty.pos.y + X_MAX - self.empty.pos.x
        if      self.empty.pos.y > self.wall.y and\
                self.wall.x != 0 and\
                self.wall.x <= self.empty.pos.x:
            reach_G += 2 * (1 + self.empty.pos.x - self.wall.x)
        return reach_G + 5 * (X_MAX - 1)

    def pairs_to_list(self) -> list[Node]:
        s = set()
        for p in self.available:
            s.add(p[0])
            s.add(p[1])
        return list(s)

# != 5 !=8 != 2 != 4
def exo1(data: list[str]) -> int:
    return Grid(data).count_available_pairs()

# 259 << 
def exo2(data: list[str]) -> int:
    return Grid(data).shortest_path()

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
            'expected': 7,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
