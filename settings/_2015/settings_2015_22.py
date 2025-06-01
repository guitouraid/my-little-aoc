import copy
from dataclasses import dataclass


READ_MODE = "lines"

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
Hit Points: 14
Damage: 8
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2015_22.txt"

class Wizard:
    def __init__(self, hits: int, dmg: int = 0) -> None:
        self.hits= hits
        self.dmg = dmg

    def armor(self) -> int:
        return 0

    def clone(self):
        return copy.deepcopy(self)


class Boss(Wizard):
    @classmethod
    def from_data(cls, data: list[str]):
        return Boss(*(int(l.split(': ')[1]) for l in data))

class Spell:
    def __init__(self, cost: int) -> None:
        self.cost = cost

    def in_use(self) -> bool:
        return False

    def usable(self, mana: int) -> bool:
        return self.cost <= mana and not self.in_use()

    def immediate(self, player: Wizard, boss: Boss):
        player.mana -= self.cost # type: ignore

    def turn(self, player: Wizard, boss: Boss):
        pass


class Missile(Spell):
    def __init__(self) -> None:
        super().__init__(53)

    def immediate(self, player: Wizard, boss: Boss):
        super().immediate(player, boss)
        boss.hits -= 4


class Drain(Spell):
    def __init__(self) -> None:
        super().__init__(73)

    def immediate(self, player: Wizard, boss: Boss):
        super().immediate(player, boss)
        player.hits += 2
        boss.hits -= 2


class Shield(Spell):
    def __init__(self) -> None:
        self._turns = 6
        self._shield = 7
        self.round = 0
        super().__init__(113)

    @property
    def shield(self) -> int:
        if self.round > 0:
            return self._shield
        return 0

    def in_use(self) -> bool:
        return self.round > 1

    def immediate(self, player: Wizard, boss: Boss):
        super().immediate(player, boss)
        self.round = self._turns

    def turn(self, player: Wizard, boss: Boss):
        if self.round > 0:
            self.round -= 1


class Poison(Spell):
    def __init__(self) -> None:
        self._turns = 6
        self.dmg = 3
        self.round = 0
        super().__init__(173)

    def in_use(self) -> bool:
        return self.round > 1

    def immediate(self, player: Wizard, boss: Boss):
        super().immediate(player, boss)
        self.round = self._turns

    def turn(self, player: Wizard, boss: Boss):
        if self.round > 0:
            boss.hits -= self.dmg
            self.round -= 1


class Recharge(Spell):
    def __init__(self) -> None:
        self._turns = 5
        self.more = 101
        self.round = 0
        super().__init__(229)

    def in_use(self) -> bool:
        return self.round > 1

    def immediate(self, player: Wizard, boss: Boss):
        super().immediate(player, boss)
        self.round = self._turns

    def turn(self, player: Wizard, boss: Boss):
        if self.round > 0:
            player.mana += self.more # type: ignore
            self.round -= 1


class Player(Wizard):
    def __init__(self, hits: int, mana: int, spells: dict) -> None:
        self.mana = mana
        self.spells = spells
        super().__init__(hits)

    def armor(self) -> int:
        return self.spells['S'].shield

class Fight:
    min_mana = 2500
    def __init__(self, data: list[str], phits: int, pmana: int, hard: bool = False) -> None:
        self.hard = hard
        self.boss = Boss.from_data(data)
        self.player = Player(phits, pmana, {
            'M': Missile(),
            'D': Drain(),
            'S': Shield(),
            'P': Poison(),
            'R': Recharge()
        })

    def player_effects(self, player: Player, boss: Boss) -> bool:
        player.spells['P'].turn(player, boss)
        player.spells['R'].turn(player, boss)
        player.spells['S'].turn(player, boss)
        return boss.hits <= 0

    def player_turn(self, player: Player, boss: Boss, spell: Spell|None) -> bool:
        if spell:
            spell.immediate(player, boss)
        return boss.hits <= 0

    def boss_turn(self, player: Player, boss: Boss) -> bool:
        player.hits -= max(1, boss.dmg - player.spells['S'].shield)
        return player.hits > 0

    def success(self, consumed):
        self.min_mana = min(self.min_mana,consumed)
        yield consumed

    def round(self, player: Player, boss: Boss, spell: Spell|None, consumed: int, chain: str):
        if self.hard:
            player.hits -= 1
            if player.hits == 0:
                return
        if self.player_effects(player, boss):
            yield from self.success(consumed)
        else:
            if spell:
                consumed += spell.cost
            win = self.player_turn(player, boss, spell)
            if win:
                yield from self.success(consumed)
            elif self.player_effects(player, boss):
                yield from self.success(consumed)
            elif self.boss_turn(player, boss):
                yield from self.next_round(player, boss, consumed, chain)

    def next_round(self, player: Player, boss: Boss, consumed: int, chain = ''):
        if consumed < self.min_mana:
            if avail := [k for k, v in player.spells.items() if v.usable(player.mana)]: # type: ignore
                for k in avail:
                    new_p = player.clone()
                    yield from self.round(new_p, boss.clone(), new_p.spells[k], consumed, chain+k)
            else:
                yield from self.round(player.clone(), boss.clone(), None, consumed, chain+'O')

def exo1(data: list[str], phits: int, pmana: int) -> int:
    simul = Fight(data, phits, pmana)
    return min(simul.next_round(simul.player, simul.boss, 0))

def exo2(data: list[str], phits: int, pmana: int) -> int:
    simul = Fight(data, phits, pmana, True)
    return min(simul.next_round(simul.player, simul.boss, 0))

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 641,
            'kw_args': {'phits': 10, 'pmana': 250}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
            'kw_args': {'phits': 50, 'pmana': 500}
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
            'kw_args': {'phits': 50, 'pmana': 500}
        },
        'runner': exo2,
    },
)
