from collections import deque
from itertools import chain, combinations
import re
from typing import Counter


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_1 = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""

TEST_DATA_2 = "" # no test 2

RE_CHIPGEN = re.compile(r'(\w+)(?:-compatible)? (microchip|generator)')

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_11.txt"

def parse_input(data: list[str]) -> list[set[tuple[str,str]]]:
    # pairs (element, type)
    return [set(RE_CHIPGEN.findall(line)) for line in data]

def invalid_transition(floor: set[tuple[str,str]]) -> bool:
    # both types present, and any generator without microchip
    return  len(set(type for _, type in floor)) == 2 and\
            any((obj, 'generator') not in floor for obj, type in floor if type == 'microchip')

def next_states(state: tuple[int,int,list[set[tuple[str,str]]]]):
    moves, elevator, floors = state
    # combinations of 1 or 2 items from current floor
    for move in chain(combinations(floors[elevator], 2), combinations(floors[elevator], 1)):
        for up_down in [1, -1]:
            next_floor = elevator + up_down
            # avoid invalid floor number
            if not 0 <= next_floor < len(floors):
                continue
            next_floors = floors.copy()
            # avoid invalid transitions
            next_floors[elevator] = next_floors[elevator].difference(move)
            if invalid_transition(next_floors[elevator]):
                continue
            next_floors[next_floor] = next_floors[next_floor].union(move)
            if invalid_transition(next_floors[next_floor]):
                continue
            yield (moves + 1, next_floor, next_floors)

def final_state(floors: list[set[tuple[str,str]]]) -> bool:
    # all floors but last are empty
    return all(not floor for level, floor in enumerate(floors) if level < len(floors) - 1)

def count_floor_objects(state: tuple[int,int,list[set[tuple[str,str]]]]) -> tuple[int,tuple[tuple[str,int]]]:
    _, elevator, floors = state
    return elevator, tuple(tuple(Counter(type for _, type in floor).most_common()) for floor in floors) # type: ignore

def min_moves_to_top(floors: list[set[tuple[str,str]]]) -> int:
    seen = set()
    queue = deque([(0,0,floors)])
    while queue:
        state = queue.popleft()
        moves, _, floors = state
        if final_state(floors):
            return moves
        for next_state in next_states(state):
            if (key := count_floor_objects(next_state)) not in seen:
                seen.add(key)
                queue.append(next_state)


def exo1(data: list[str]) -> int:
    return min_moves_to_top(parse_input(data))

additional = {
    ('elerium', 'generator'),
    ('elerium', 'microchip'),
    ('dilithium', 'generator'),
    ('dilithium', 'microchip'),
}

def exo2(data: list[str]) -> int:
    floors = parse_input(data)
    floors[0] |= additional
    return min_moves_to_top(floors)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 11,
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
