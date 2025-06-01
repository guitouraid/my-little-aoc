READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_8.txt"

class Screen:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.display = [['.']*cols for _ in range(rows)]

    def lit(self) -> int:
        return sum(self.display[r][c] == '#' for r in range(self.rows) for c in range(self.cols))

    def rectangle(self, cols: int, rows: int):
        for r in range(rows):
            for c in range(cols):
                self.display[r][c] = '#'

    def rotate_row(self, row: int, offset: int):
        next_row = [self.display[row][(col-offset)%self.cols] for col in range(self.cols)]
        for col in range(self.cols):
            self.display[row][col] = next_row[col]

    def rotate_col(self, col: int, offset: int):
        next_col = [self.display[(row-offset)%self.rows][col] for row in range(self.rows)]
        for row in range(self.rows):
            self.display[row][col] = next_col[row]

    def process(self, instruction: str):
        match (sp:=instruction.split())[0]:
            case 'rect':
                self.rectangle(*(int(x) for x in sp[1].split('x')))
            case 'rotate':
                idx = int(sp[2].split('=')[1])
                by = int(sp[-1])
                match sp[1]:
                    case 'row':
                        self.rotate_row(idx, by)
                    case 'column':
                        self.rotate_col(idx, by)
                    case _:
                        raise ValueError(f'Invalid axis {sp[1]} in {instruction} ?')

            case _:
                raise ValueError(f'Invalid instruction ? {instruction}')

def exo1(data: list[str], rows: int, cols: int) -> int:
    scr = Screen(rows, cols)
    for line in data:
        scr.process(line)
    return scr.lit()

def exo2(data: list[str], rows: int, cols: int) -> None:
    scr = Screen(rows, cols)
    for line in data:
        scr.process(line)
    print('\n'.join([''.join(r) for r in scr.display]).replace('.', ' '))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 6,
            'kw_args': {'rows': 3,'cols': 7}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
            'kw_args': {'rows': 6,'cols': 50}
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
            'kw_args': {'rows': 6,'cols': 50}
        },
        'runner': exo2,
    },
)
