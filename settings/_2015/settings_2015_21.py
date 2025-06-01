

READ_MODE = "lines"

ARMORY = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
Hit Points: 12
Damage: 7
Armor: 2
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2015_21.txt"

class Item(tuple[int,int,int]):
    @property
    def cost(self) -> int:
        return self.__getitem__(0)
    @property
    def damage(self) -> int:
        return self.__getitem__(1)
    @property
    def armor(self) -> int:
        return self.__getitem__(2)


class Equip(tuple[Item,Item,Item,Item]):
    @property
    def cost(self) -> int:
        return sum(i.cost for i in self if i)
    @property
    def damage(self) -> int:
        return sum(i.damage for i in self if i)
    @property
    def armor(self) -> int:
        return sum(i.armor for i in self if i)


class Armory:
    def __init__(self) -> None:
        self.items = {}
        type = None
        for line in ARMORY.splitlines():
            if line:
                s = line.split()
                if s[0].endswith(':'):
                    self.items[type := s[0][:-1]] = []
                else:
                    self.items[type].append(Item(int(x) for x in s[-3:]))

    def combinations(self):
        for w in self.items['Weapons']:
            for a in self.items['Armor'] + [None]:
                for rr in self.items['Rings'] + [None]:
                    for lr in self.items['Rings'] + [None]:
                        if rr and rr == lr:
                            continue
                        yield Equip((w,a,rr,lr))


class Fighter:
    def __init__(self, hits: int, dmg: int, arm: int) -> None:
        self.hits = hits
        self.dmg = dmg
        self.arm = arm

    def wins(self, other) -> bool:
        whits = self.hits
        bhits = other.hits
        wdmg = max(1,self.dmg-other.arm)
        bdmg = max(1,other.dmg-self.arm)
        while True:
            if (bhits := bhits - wdmg) <= 0:
                return True
            if (whits := whits - bdmg) <= 0:
                return False

def parse_input(data: list[str]) -> Fighter:
    return Fighter(*(
        int(line.split(': ')[1])
        for line in data
    ))

def exo1(data: list[str], hits: int) -> int:
    boss = parse_input(data)
    return min(
        e.cost for e in Armory().combinations() if Fighter(hits, e.damage, e.armor).wins(boss)
    )

def exo2(data: list[str]) -> int:
    boss = parse_input(data)
    return max(
        e.cost for e in Armory().combinations() if not Fighter(100, e.damage, e.armor).wins(boss)
    )

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 65,
            'kw_args': {'hits': 8},
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
            'kw_args': {'hits': 100},
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
