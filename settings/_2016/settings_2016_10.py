from math import prod
from operator import mul
import re
from collections.abc import Callable

READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2016_10.txt"

RE_BOT = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')
RE_VALUE = re.compile(r'value (\d+) goes to bot (\d+)')

class Processable:
    pass

class Input(Processable):
    def __init__(self, value: str) -> None:
        self._value = int(value)

    def value(self) -> int:
        return self._value

class Output(Processable):
    def __init__(self, depend: Callable) -> None:
        self.depend = depend
        self._value = None

    def value(self) -> int:
        if not self._value:
            self._value = self.depend()
        return self._value

class Bot:
    def __init__(self) -> None:
        self.depends = []
        self._values = set()

    def add(self, depend: Callable) -> None:
        self.depends.append(depend)

    def equals(self, values: tuple[int,int]) -> bool:
        return set(values) == self._values

    def _compute(self) -> None:
        if len(self.depends) != 2:
            raise ValueError('Invalid bot')
        self._values = {s() for s in self.depends}

    def low(self) -> int:
        if len(self._values) != 2:
            self._compute()
        return min(self._values)

    def high(self) -> int:
        if len(self._values) != 2:
            self._compute()
        return max(self._values)


class BotNet:
    def __init__(self, data: list[str]) -> None:
        self.bots: dict[int,Bot] = {}
        self.outputs: dict[int,Output] = {}
        for line in data:
            if m := RE_VALUE.match(line):
                input, bot_id = m.groups()
                self.bots.setdefault(int(bot_id), Bot()).add(Input(input).value)
            elif m := RE_BOT.match(line):
                bot_id, ltt, lti, htt, hti = m.groups()
                bot_id = int(bot_id)
                src_bot = self.bots.setdefault(int(bot_id), Bot())
                match ltt:
                    case 'bot':
                        self.bots.setdefault(int(lti), Bot()).add(src_bot.low)
                    case 'output':
                        self.outputs[int(lti)] = Output(src_bot.low)
                    case _:
                        raise ValueError(f'Invalid target type {ltt}')
                match htt:
                    case 'bot':
                        self.bots.setdefault(int(hti), Bot()).add(src_bot.high)
                    case 'output':
                        self.outputs[int(hti)] = Output(src_bot.high)
                    case _:
                        raise ValueError(f'Invalid target type {htt}')

    def compute(self) -> dict[int,int]:
        return {k : v.value() for k, v in self.outputs.items()}

    def get_bot(self, values: tuple[int,int]) -> int:
        for k, b in self.bots.items():
            if b.equals(values):
                return k
        raise ValueError(f'No bot with values {values}')

def exo1(data: list[str], values: list[int]) -> int:
    bn = BotNet(data)
    bn.compute()
    return bn.get_bot(tuple(values))

def exo2(data: list[str]) -> int:
    bn = BotNet(data)
    bn.compute()
    return prod(v.value() for k, v in bn.outputs.items() if k in (0,1,2))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 2,
            'kw_args': {'values': [2,5]}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
            'kw_args': {'values': [17,61]}
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 30,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
