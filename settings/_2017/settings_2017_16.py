READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
s1,x3/4,pe/b
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_16.txt"


class DancingProgs:
    def __init__(self, data: str, seed: str) -> None:
        self.chore = data.split(',')
        self.progs = seed
        self.len = len(seed)

    def _swap_pos(self, pos: tuple[int,int]) -> None:
        mini, maxi = sorted(pos)
        self.progs = f'{self.progs[:mini]}{self.progs[maxi]}{self.progs[mini+1:maxi]}{self.progs[mini]}{self.progs[maxi+1:]}'

    def _swap_letters(self, first: str, second: str) -> None:
        self._swap_pos((self.progs.find(first), self.progs.find(second)))

    def _spin(self, length: int) -> None:
        pos = self.len -length
        self.progs = f'{self.progs[pos:]}{self.progs[:pos]}'

    def _step(self, move: str) -> None:
        instr = move[0]
        match instr:
            case 's':
                self._spin(int(move[1:]))
            case 'x':
                self._swap_pos(tuple(map(int, move[1:].split('/')))) # type: ignore
            case 'p':
                self._swap_letters(*move[1:].split('/'))

    def dance(self) -> None:
        for p in self.chore:
            self._step(p)

def iterate(dp: DancingProgs, times: int) -> str:
    memo = dp.progs
    for i in range(times):
        dp.dance()
        if dp.progs == memo:
            return iterate(dp, times % (i + 1))
    return dp.progs

def exo1(data: str, seed: str) -> str:
    dp = DancingProgs(data, seed)
    dp.dance()
    return dp.progs

def exo2(data: str, seed: str) -> str:
    dp = DancingProgs(data, seed)
    return iterate(dp, 1000000000)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 'baedc',
            'kw_args': {'seed': 'abcde'}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_1,
            'kw_args': {'seed': 'abcdefghijklmnop'}
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 'abcde',
            'kw_args': {'seed': 'abcde'}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
            'kw_args': {'seed': 'abcdefghijklmnop'}
        },
        'runner': exo2,
    },
)
