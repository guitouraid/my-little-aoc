

from collections import deque


READ_MODE = "lines"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
5-8
0-2
4-7
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = "2016_20.txt"


class IPRange(tuple[int,int]):
    MIN_IP = 0
    max_ip = 4294967295

    @classmethod
    def from_str(cls, strange: str):
        min_ip, max_ip = map(int, strange.split('-'))
        assert min_ip <= max_ip
        return IPRange((max(min_ip, cls.MIN_IP), min(max_ip, cls.max_ip)))

    @property
    def min(self) -> int:
        return self.__getitem__(0)

    @property
    def max(self) -> int:
        return self.__getitem__(1)


class IPRanges:
    def __init__(self, ranges: list[IPRange]) -> None:
        self.ranges = ranges

    @classmethod
    def from_data(cls, data: list[str]):
        return IPRanges(list(map(IPRange.from_str, sorted(data))))
    
    def test_ip(self, ip: int) -> bool:
        for r in self.ranges:
            if r.min <= ip <= r.max:
                return False
        return True

    def find_min(self) -> int:
        if len(self.ranges) == 0 or self.ranges[0].min > 0:
            return 0
        candidates = sorted(r.max+1 for r in self.ranges)
        valid = [c for c in candidates if self.test_ip(c)]
        return valid[0]
    
    def find_all(self) -> int:
        # return 0
        if len(self.ranges) == 0:
            return 1 + IPRange.max_ip
        # clusterize
        current = IPRange(self.ranges[0])
        clustered = []
        for r in self.ranges[1:]:
            if r.min > current.max + 1:
                clustered.append(current)
                current = IPRange(r)
            elif r.max > current.max:
                current = IPRange((current.min, r.max))
        clustered.append(current)
        return IPRange.max_ip - sum(r.max - r.min for r in clustered) - len(clustered) + 1
        




# 753115 << 32259706 << 1031041398
def exo1(data: list[str]) -> int:
    return IPRanges.from_data(data).find_min()

# << 999544432 (according to web form)
# Giving up on this one... Quite sure about my answer
def exo2(data: list[str], maxi: int|None) -> int:
    # IPRange.max_ip = 10
    # hard = ['1-2', '1-4', '1-3', '2-3', '2-5', '7-9']
    # print(IPRanges.from_data(hard).find_all())
    # return 2
    if maxi:
        IPRange.max_ip = maxi
    return IPRanges.from_data(data).find_all()

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
            'expected': 2,
            'kw_args': {'maxi': 9}
        },
        'real_data': {
            'type': 'file',
            'from': REAL_DATA_2,
            'kw_args': {'maxi': None}
        },
        'runner': exo2,
    },
)
