from collections import deque
from copy import copy
from itertools import permutations
from typing import NamedTuple


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_24.txt"


class Position(NamedTuple):
    x: int
    y: int


class Grid:
    def __init__(self, data: list[str]) -> None:
        self.grid: list[str] = data
        self.walls, self.targets = self._set_wt()
        self.distances = self._distances()
        self._set_wt()

    def _set_wt(self) -> tuple[set[Position],dict[int, Position]]:
        walls = set()
        targets = {}
        for y, line in enumerate(self.grid):
            for x, c in enumerate(line):
                match c:
                    case '#':
                        walls.add(Position(x, y))
                    case '.':
                        pass
                    case _:
                        targets[int(c)] = Position(x, y)
        return walls, targets

    def _dist(self, start: Position, dest: Position) -> int:
        visited = {start}
        visits = deque([[start]])
        while visits:
            visit = visits.popleft()
            current = visit[-1]
            if current == dest:
                return len(visit) - 1
            for move in self._get_moves((current)):
                if move not in visited and move not in self.walls:
                    next_visit = copy(visit)
                    next_visit.append(move)
                    visits.append(next_visit)
                    visited.add(move)
        raise ValueError('Must have messed with smth!')

    def _distances(self) -> dict[tuple[int,int],int]:
        results = {}
        length = len(self.targets)
        for i in range(length):
            for j in range(i + 1, length):
                results[(i,j)] = results[(j,i)] = self._dist(self.targets[i], self.targets[j])
        return results

    def __str__(self) -> str:
        return '\n'.join(self.grid)

    def _get_moves(self, pos: Position) -> list[Position]:
         return [
            neighbour for neighbour in [
                Position(pos.x+1, pos.y),
                Position(pos.x-1, pos.y),
                Position(pos.x, pos.y+1),
                Position(pos.x, pos.y-1),
            ] if neighbour not in self.walls
        ]

    def _steps_count(self, combo: list[int], loop: bool=False) -> int:
        actual = [0] + combo
        if loop:
            actual = actual + [0]
        return sum(self.distances[(i,j)] for i, j in zip(actual, actual[1:]))

    def min_dist(self, loop: bool=False) -> int:
        return min(self._steps_count(list(combo), loop) for combo in permutations(range(1, len(self.targets))))


def exo1(data: list[str]) -> int:
    grid = Grid(data)
    # print(str(grid))
    # print()
    return grid.min_dist()

def exo2(data: list[str]) -> int:
    grid = Grid(data)
    return grid.min_dist(True)

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
            'from': REAL_DATA_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 20,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
