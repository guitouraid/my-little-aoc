from collections import deque
from copy import copy


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_21.txt"

class Scrambler:
    def __init__(self, ops: list[str], revert: bool = False) -> None:
        self.ops = ops
        self.revert = revert
        if revert:
            self._fn_rot_l = self._rot_r
            self._fn_rot_r = self._rot_l
            self._fn_rot_p = self._rev_rot_p
            self._fn_move = self._rev_move
        else:
            self._fn_rot_l = self._rot_l
            self._fn_rot_r = self._rot_r
            self._fn_rot_p = self._rot_p
            self._fn_move = self._move

    def scramble(self, word: str) -> str:
        ops = self.ops
        if self.revert:
            ops = ops[::-1]
        for line in ops:
            word = self.operate(line, word)
        return word

    def operate(self, line: str, target: str) -> str:
        op = deque(line.split())
        match cmd := op.popleft():
            case 'swap':
                return self._swap(op, target)
            case 'reverse':
                return self._rev(op, target)
            case 'rotate':
                return self._rot(op, target)
            case 'move':
                op.popleft()
                return self._fn_move(target, int(op.popleft()), int(op.pop()))
            case _:
                raise ValueError(f'Unmatched operation {cmd}')
 
    def _swap(self, op: deque, target: str) -> str:
        match sub := op.popleft():
            case 'position':
                return self._swap_p(op, target)
            case 'letter':
                return self._swap_l(op, target)
            case _:
                raise ValueError(f'Unmatched swap operation {sub}')

    def _swap_p(self, op: deque, target: str) -> str:
        return self._actual_swap(target, int(op.popleft()), int(op.pop()))

    def _swap_l(self, op: deque, target: str) -> str:
        return self._actual_swap(target, target.find(op.popleft()), target.find(op.pop()))

    def _actual_swap(self, target: str, minoumax: int, maxoumin) -> str:
        mini, maxi = sorted((minoumax, maxoumin))
        return f'{target[:mini]}{target[maxi]}{target[mini+1:maxi]}{target[mini]}{target[maxi+1:]}'

    def _rev(self, op: deque, target: str) -> str:
        op.popleft()
        mini, maxi = sorted((int(op.popleft()), int(op.pop())))
        return f'{target[:mini]}{target[mini:maxi+1][::-1]}{target[maxi+1:]}'

    def _rot(self, op: deque, target: str) -> str:
        match sub := op.popleft():
            case 'left':
                return self._fn_rot_l(target, int(op.popleft()))
            case 'right':
                return self._fn_rot_r(target, int((op.popleft())))
            case _:
                return self._fn_rot_p(target, op.pop())

    def _rot_l(self, target: str, steps: int) -> str:
        for _ in range(steps):
            target = f'{target[1:]}{target[0]}'
        return target

    def _rot_r(self, target: str, steps: int) -> str:
        for _ in range(steps):
            target = f'{target[-1]}{target[0:-1]}'
        return target

    def _rot_p(self, target: str, letter: str) -> str:
        steps = target.find(letter)
        if steps > 3:
            steps += 1
        return self._rot_r(target, (steps+1)%len(target))

    def _rev_rot_p(self, target: str, letter: str) -> str:
        candidate = copy(target)
        # keep brute force: observable pattern for len 8, but did not find for len 5 (or others)
        while True:
            candidate = f'{candidate[1:]}{candidate[0]}'
            if self._rot_p(candidate, letter) == target:
                return candidate

    def _move(self, target: str, from_pos: int, to_pos: int) -> str:
        letter = target[from_pos]
        target = f'{target[:from_pos]}{target[from_pos+1:]}'
        return f'{target[:to_pos]}{letter}{target[to_pos:]}'

    def _rev_move(self, target: str, from_pos: int, to_pos: int) -> str:
        return self._move(target, to_pos, from_pos)


def exo1(data: list[str], word: str) -> str:
    return Scrambler(data).scramble(word)

def exo2(data: list[str], word: str) -> str:
    return Scrambler(data, True).scramble(word)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 'decab',
            'kw_args': {'word': 'abcde'}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_1,
            'kw_args': {'word': 'abcdefgh'}
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 'abcde',
            'kw_args': {'word': 'decab'}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
            'kw_args': {'word': 'fbgdceah'}
        },
        'runner': exo2,
    },
)
