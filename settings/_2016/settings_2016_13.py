from functools import lru_cache


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
10
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
1350
"""

@lru_cache
def is_even_bin(x: int, y: int, offset: int) -> bool:
    value = x * (x + 3) + y * (2 * x + y + 1) + offset
    ones = '{0:b}'.format(value).count('1')
    return ones % 2 == 0

class Position(tuple[int,int]):
    @property
    def x(self) -> int:
        return self.__getitem__(0)

    @property
    def y(self) -> int:
        return self.__getitem__(1)

    def is_reachable(self, offset: int)-> bool:
        return  self.x >= 0 and self.y >= 0 and \
                is_even_bin(self.x, self.y, offset)


class MazePath:
    def __init__(self, offset: int, positions: list[Position]|None = None) -> None:
        self.offset = offset
        self.positions = positions or [Position((1,1))]

    def next_moves(self):
        current = self.positions[-1]
        for next_move in (
            Position((current.x + 1, current.y)),
            Position((current.x, current.y + 1)),
            Position((current.x - 1, current.y)),
            Position((current.x, current.y - 1)),
        ):
            if next_move.is_reachable(self.offset) and next_move not in self.positions:
                yield next_move

    def clone(self):
        return MazePath(self.offset, self.positions.copy())

class MazeWalker:
    def __init__(self, offset: int, explore: list[MazePath]|None = None) -> None:
        self.start = MazePath(offset)
        self.explore = explore or [self.start]

    def fastest_path(self, goal: Position) -> int:
        while self.explore:
            current_path = self.explore.pop(0)
            current_pos = current_path.positions[-1]
            if current_pos == goal:
                return len(current_path.positions) - 1
            for move in current_path.next_moves():
                next_path = current_path.clone()
                next_path.positions.append(move)
                self.explore.append(next_path)
        raise ValueError(f'Found no path from {self.start} to {goal}')

    def max_visited(self, steps: int, visited: list[Position]) -> int:
        next_explore = []
        for e in self.explore:
            if (pos := e.positions[0]) not in visited:
                visited.append(pos)
                for next_move in e.next_moves():
                    if next_move.is_reachable(self.start.offset) and next_move not in visited:
                        next_explore.append(MazePath(self.start.offset, [next_move]))
        if steps == 0:
            return len(visited)
        return MazeWalker(self.start.offset, next_explore).max_visited(steps - 1, visited)

        

def exo1(data: str, goal: tuple[int,int]) -> int:
    offset = int(data.strip())
    return MazeWalker(offset).fastest_path(Position(goal))

def exo2(data: str, steps: int) -> int:
    offset = int(data.strip())
    return MazeWalker(offset).max_visited(steps, [])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 11,
            'kw_args': {'goal': (7,4)}
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_1,
            'kw_args': {'goal': (31,39)}
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 11,
            'kw_args': {'steps': 5}
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
            'kw_args': {'steps': 50}
        },
        'runner': exo2,
    },
)
