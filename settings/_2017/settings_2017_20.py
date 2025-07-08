from collections import defaultdict
from typing import NamedTuple, Self


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_1 = """
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
"""

TEST_DATA_2 = """
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<1,0,0>, a=<0,0,0>
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2017_20.txt"

class SpaceVect(NamedTuple):
    x: int
    y: int
    z: int

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


class Trajectory(NamedTuple):
    pos: SpaceVect
    speed: SpaceVect
    accel: SpaceVect

    def next_tick(self):
        next_speed = SpaceVect(self.speed.x+self.accel.x, self.speed.y+self.accel.y, self.speed.z+self.accel.z)
        next_pos = SpaceVect(self.pos.x+next_speed.x, self.pos.y+next_speed.y, self.pos.z+next_speed.z)
        return Trajectory(next_pos, next_speed, self.accel)


def parse(line: str) -> Trajectory:
    pva = line.split(', ')
    p = SpaceVect(*(int(v) for v in pva[0].split('=')[1][1:-1].split(',')))
    s = SpaceVect(*(int(v) for v in pva[1].split('=')[1][1:-1].split(',')))
    a = SpaceVect(*(int(v) for v in pva[2].split('=')[1][1:-1].split(',')))
    return Trajectory(p, s, a)


class Particles:
    MAX_TICK = 1000000
    def __init__(self, data: list[str]) -> None:
        self.particles = [parse(line) for line in data]

    def next_tick(self) -> None:
        by_pos = defaultdict(list)
        for p in self.particles:
            next_p = p.next_tick()
            by_pos[next_p.pos].append(next_p)
        self.particles = [ps[0] for ps in by_pos.values() if len(ps) == 1]


def exo1(data: list[str]) -> int:
    particles = [parse(line) for line in data]
    return min(enumerate(particles), key=lambda t: (t[1].accel.manhattan(), t[1].speed.manhattan(), t[1].pos.manhattan()))[0]

def exo2(data: list[str]) -> int:
    particles = Particles(data)
    for _ in range(Particles.MAX_TICK):
        particles.next_tick()
    return len(particles.particles)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 0,
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
            'expected': 1,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)