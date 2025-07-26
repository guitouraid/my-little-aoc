READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_21.txt"


class FractalGen:
    INIT = """\
.#.
..#
###\
"""

    def __init__(self, data: list[str]) -> None:
        self.pattern: list[str] = str(self.INIT).split('\n')
        self.transforms = self._parse_input(data)

    def _parse_input(self, data: list[str]) -> dict[tuple[str],list[str]]:
        d = {}
        for line in data:
            m, r = self._parse_line(line)
            for v in self._variants(m):
                d[tuple(v)] = r
        return d

    def _parse_line(self, line: str) -> tuple[list[str],list[str]]:
        matching, resulting = line.split(' => ')
        return(matching.split('/'),resulting.split('/'))

    def _variants(self, matching: list[str]) -> list[list[str]]:
        opts = {tuple(matching)}
        flip = [m[::-1] for m in matching]
        opts.add(tuple(flip))
        for _ in range(4):
            matching = [''.join(l) for l in zip(*matching[::-1])]
            opts.add(tuple(matching))
        return [list(opt) for opt in opts]

    def _split2_3(self, pattern: list[str]):
        splitted = []
        q, r = divmod(len(pattern), 2)
        qq, rr = divmod(len(pattern), 3)
        if r == 0:
            for j in range(q):
                splitted.append([])
                for i in range(q):
                    splitted[j].append([])
                    for jj in range(2):
                        splitted[j][i].append(pattern[j+jj][j:j+2])
        elif rr == 0:
            for j in range(qq):
                splitted.append([])
                for i in range(qq):
                    splitted[j].append([])
                    for jj in range(3):
                        splitted[j][i].append(pattern[j+jj][j:j+3])
        else:
            raise ValueError(f'Weird length: {len(pattern)}')
        return splitted

    def _rejoin(self, patterns):
        joined = []
        for pl in patterns:
            for j in range(len(pl)):
                # to be continued
                # joined.append(map(concat))
                joined.append(''.join(pl[j]))
        return joined

    def iterate(self):
        splitted = self._split2_3(self.pattern)
        for j in range(len(splitted)):
            for i in range(len(splitted[j])):
                try:
                    splitted[j][i] = self.transforms[tuple(splitted[j][i])]
                except KeyError:
                    raise ValueError(f'Should have found a match for {splitted[j][i]}')
        self.pattern = self._rejoin(splitted)

def exo1(data: list[str], rounds: int) -> int:
    fg = FractalGen(data)
    for _ in range(rounds):
        fg.iterate()
    return sum(s.count('#') for s in fg.pattern)

def exo2(data: list[str]) -> int:
    return 0

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 0,
            'kw_args': {'rounds': 2}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_1,
            'kw_args': {'rounds': 5}
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
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)