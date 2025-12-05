from functools import reduce


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2025_5.txt"

def parse_input(data: list[str]) -> tuple[list[range],list[int]]:
    fresh = []
    ingredients = []
    first = True
    for line in data:
        if line:
            if first:
                low, high = map(int, line.split('-'))
                fresh.append(range(low, high+1))
            else:
                ingredients.append(int(line))
        else:
            first = False
    return (fresh, ingredients)

def is_fresh(ingredient: int, known_fresh: list[range]) -> bool:
    for r in known_fresh:
        if ingredient in r:
            return True
    return False

def exo1(data: list[str]) -> int:
    fresh, check = parse_input(data)
    return sum([is_fresh(i, fresh) for i in check])

def exo2(data: list[str]) -> int:
    fresh, _ = parse_input(data)
    fresh.sort(key=lambda r: (r.start, r.stop), reverse=True)
    r = fresh.pop()
    count = 0
    while fresh:
        next_r = fresh.pop()
        if next_r.start > r.stop:
            count += len(r)
            r = next_r
        else:
            r = range(r.start , max([r.stop, next_r.stop]))
    return count + len(r)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 3,
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
            'expected': 14,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)