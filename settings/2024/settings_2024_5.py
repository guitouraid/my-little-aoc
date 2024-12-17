from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_ALL

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2024_5_1.txt"

def break_data(data: str) -> tuple[list[str], list[str]]:
    current = one = []
    two = []
    for line in data.split('\n'):
        if line == '':
            current = two
        else:
            current.append(line)
    return (one, two)

def score_on_rules(rules: list[str], listing: str) -> int:
    pages = listing.split(',')
    count = len(pages)
    for i in range(count-1):
        for j in range(i+1, count):
            if f"{pages[j]}|{pages[i]}" in rules:
            # if f"{pages[i]}|{pages[j]}" not in rules:
                return 0
    return int(pages[int((count-1)/2)])

class Node:
    def __init__(self, value:str, before=None, after=None) -> None:
        self.value=value
        self.previous=before
        self.next=after

class Ordered:
    LEFT = 0
    RIGHT = 1
    def __init__(self, rules: list[str], listing: str) -> None:
        self.rules=rules
        self.start=self.current=None
        for number in listing.split(','):
            self.insert(Node(number))

    def reset(self):
        self.current=self.start

    def insert_before(self, node: Node) -> Node:
        node.previous = self.current.previous
        node.next = self.current
        self.current.previous.next = node
        self.current.previous = node
        self.current = node
        return node

    def insert_after(self, node: Node) -> Node:
        node.previous = self.current
        node.next = self.current.next
        self.current.next.previous = node
        self.current.next = node
        self.current = node
        return node

    def propagate_left(self, node: Node) -> Node:
        if self.current.previous is None:
            node.next = self.current
            self.current.previous = node
            if self.start == self.current:
                self.start = node
            self.current = node
            return node
        else:
            self.current = self.current.previous
            return self.insert(node, self.LEFT)

    def propagate_right(self, node: Node) -> Node:
        if self.current.next is None:
            node.previous = self.current
            self.current.next = node
            self.current = node
            return node
        else:
            self.current = self.current.next
            return self.insert(node, self.RIGHT)

    def insert(self, node: Node, propagate=None) -> Node:
        if self.start is None:
            self.start=self.current=node
            return node
        else:
            cv = self.current.value
            nv = node.value
            if f'{cv}|{nv}' in self.rules:
                if propagate == self.LEFT:
                    return self.insert_after(node)
                return self.propagate_right(node)
            elif f'{nv}|{cv}' in self.rules:
                if propagate == self.RIGHT:
                    return self.insert_before(node)
                return self.propagate_left(node)
            else:
                raise ValueError("Unexpected case !")

    def list(self) -> list[str]:
        lst = []
        current = self.start
        while current:
            lst.append(current.value)
            current = current.next
        return lst

    def middle_value(self) -> int:
        lst = self.list()
        return int(lst[int((len(lst)-1)/2)])


def reorder_page(rules: list[str], listing: str) -> int:
    return str(Ordered(rules, listing))

def exo1(data: str) -> Any:
    rules, prints = break_data(data.strip())
    return sum([score_on_rules(rules, listing) for listing in prints])

def exo2(data: str) -> Any:
    rules, prints = break_data(data.strip())
    return sum([Ordered(rules, listing).middle_value() for listing in prints if score_on_rules(rules, listing)==0])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 143,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_1,
        },
        'runner': exo1,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_2,
            'expected': 123,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)