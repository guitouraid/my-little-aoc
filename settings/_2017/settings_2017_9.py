from collections import deque


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_1 = """
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{<a>,<a>,<a>,<a>}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}
"""

TEST_DATA_2 = """
<>
<random characters>
<<<<>
<{!>}>
<!!>
<!!!>>
<{o"i!a,<{i<a>
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_9.txt"

def parse_line(line: str) -> tuple[int,int]:
    in_garbage = False
    score = gcount = depth = 0
    q = deque(line)
    while q:
        match c := q.popleft():
            case '!':
                q.popleft()
            case '>':
                in_garbage = False
            case _ if in_garbage:
                gcount += 1
            case '<':
                in_garbage = True
            case '{':
                depth += 1
            case '}':
                score += depth
                depth -= 1
    return score, gcount               



def exo1(data: list[str]) -> list[int]:
    return [score for score, _ in map(parse_line, data)]

def exo2(data: list[str]) -> list[int]:
    return [gcount for _, gcount in map(parse_line, data)]

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': [1, 6, 5, 16, 1, 9, 9, 3],
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
            'expected': [0, 17, 3, 2, 0, 0, 10],
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
