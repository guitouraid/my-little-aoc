from itertools import combinations
from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2024_8_1.txt"

class Node(tuple[int,int]):
    pass

    @property
    def line(self):
        return self.__getitem__(0)

    @property
    def index(self):
        return self.__getitem__(1)

class NodeValidator:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def node(self, line, index) -> Node:
        if line < 0 or index < 0 or line >= self.height or index >= self.width:
            return None
        return Node((line, index))

class NodesPair(tuple[Node,Node]):
    # def __init__(self, nodes: tuple[Node,Node]):
    #     super().__init__(nodes)

    @property
    def first(self):
        return self.__getitem__(0)

    @property
    def second(self):
        return self.__getitem__(1)

    def antinodes(self, validator: NodeValidator) -> list[Node]:
        ret = []
        for n1, n2 in ((self.first, self.second), (self.second, self.first)):
            anti = validator.node(
                n1.line*2-n2.line,
                n1.index*2-n2.index
            )
            if anti:
                ret.append(anti)
        return ret

    def more_antinodes(self, validator: NodeValidator) -> list[Node]:
        ret = []
        o_l = self.first.line
        o_r = self.first.index
        d_l = self.first.line - self.second.line
        d_r = self.first.index -self.second.index
        i = 0
        while anti := validator.node(o_l-i*d_l, o_r-i*d_r):
            ret.append(anti)
            i += 1
        i = 1
        while anti := validator.node(o_l+i*d_l, o_r+i*d_r):
            ret.append(anti)
            i += 1
        return ret


class NodeSet(set[Node]):
    def pairs(self) -> list[NodesPair]:
        make_pair = lambda pair: NodesPair(pair)
        return list(map(make_pair, combinations(self, 2)))

class Map:
    def __init__(self, data: list[str]):
        self.validator = NodeValidator(len(data), len(data[0]))
        self.nodes = {}
        for i in range(self.validator.height):
            for j in range(self.validator.width):
                atype = data[i][j]
                if atype != '.':
                    self.nodes.setdefault(atype, NodeSet()).add(Node((i, j)))

    def _antinodes(self,fun: callable) -> NodeSet:
        antinodes = NodeSet()
        for nodes in self.nodes.values():
            for pair in nodes.pairs():
                antinodes.update(pair.antinodes(self.validator))
        return antinodes

    def antinodes(self, fun: callable) -> NodeSet:
        antinodes = NodeSet()
        for nodes in self.nodes.values():
            for pair in nodes.pairs():
                antinodes.update(fun(pair, self.validator))
        return antinodes


def exo1(data: list[str]|str) -> Any:
    return len(Map(data).antinodes(NodesPair.antinodes))

def exo2(data: list[str]|str) -> Any:
    return len(Map(data).antinodes(NodesPair.more_antinodes))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 14,
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
            'expected': 34,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)