from collections import deque
from itertools import count
import time


READ_MODE = "all"

### test/real data as raw string ...
TEST_DATA_2 = TEST_DATA_1 = """
5
"""

### ... or file (store file under `DATA_DIR`)

REAL_DATA_2 = REAL_DATA_1 = """
3005290
"""

class Timer:
    def __init__(self) -> None:
        self._start = time.perf_counter()

    def elapsed(self):
        return time.perf_counter() - self._start


class IntNode:
    def __init__(self, value: int, following=None) -> None:
        self.value = value
        self.following = following

    def __str__(self) -> str:
        return f"{self.value} -> "


class Circle:
    def __init__(self, size: int) -> None:
        assert size > 0
        self.size = size
        self.current =  head = IntNode(1)
        for i in range(self.size, 1, -1):
            node = IntNode(i, head)
            head = node
        self.current.following = head

    def kill_opposite(self):
        assert self.size > 1
        before = self.current
        for _ in range(self.size//2-1):
            before = before.following # type: ignore
        before.following = before.following.following # type: ignore
        self.size -= 1

    def __str__(self) -> str:
        chain = ""
        current = self.current
        for _ in range(self.size):
            chain += str(current)
            current = current.following # type: ignore
        return f"start: {chain}"


class WhiteElephantParty:
    def __init__(self, elves: int) -> None:
        self.elves = elves

    # too slow
    # def gifted_elf(self) -> int:
    #     elves = list(range(1, self.elves+1))
    #     i = 0
    #     while (remaining := len(elves)) > 1:
    #         if remaining % 10000 == 0:
    #             print(f'Remaining: {remaining}')
    #         next_i = (i + 1) % remaining
    #         elves.pop(next_i)
    #         if next_i:
    #             i += 1
    #         else:
    #             i = 0
    #     return elves[0]

    # quite slow but acceptable
    # def gifted_elf(self) -> int:
    #     def inc(i: int) -> int:
    #         return (i + 1) % self.elves
    #     gifted = [True] * self.elves
    #     last = 0
    #     drop = 1
    #     while last != drop:
    #         gifted[drop] = False
    #         last = inc(drop)
    #         while not gifted[last]:
    #             last = inc(last)
    #         drop = inc(last)
    #         while not gifted[drop]:
    #             drop = inc(drop)
    #     return last+1

    # the recursive k=2 case from https://en.wikipedia.org/wiki/Josephus_problem
    # def gifted_elf_next(self) -> int:
    #     def recurse(n: int) -> int:
    #         if n == 1:
    #             return 1
    #         return 2 * recurse(n // 2) - pow(-1, n)
    #     return recurse(self.elves)

    # the analytics solution from https://en.wikipedia.org/wiki/Josephus_problem
    # def gifted_elf_next(self) -> int:
    #     m = self.elves.bit_length() - 1
    #     l = self.elves - pow(2, m)
    #     return 2 * l + 1

    # the binary trick for analytic solution
    def gifted_elf_next(self) -> int:
        b = f"{self.elves:b}"
        return int(f"{b[1:]}{b[0]}", 2)

    # the general case from https://en.wikipedia.org/wiki/Josephus_problem
    # too many recursions
    # def gifted_elf_gen(self, next: int) -> int:
    #     def recurse(n: int, k: int) -> int:
    #         if n == 1:
    #             return 0
    #         return (recurse(n-1, k) + k) % n
    #     return recurse(self.elves, next) + 1

    # too slow
    # def gifted_elf_opposite(self) -> int:
    #     active = list(range(1, self.elves+1))
    #     last = 0
    #     remaining = self.elves
    #     while remaining > 1:
    #         if remaining % 100000 == 0:
    #             print(f"Remaining {remaining}")
    #         next = (last + remaining // 2) % remaining
    #         active.pop(next)
    #         remaining -= 1
    #         if next > last:
    #             last = (last+1)%remaining
    #         else:
    #             last %= remaining
    #     return active[0]

    # even slower than above!
    # def gifted_elf_opposite(self) -> int:
    #     gifted = [True] * self.elves
    #     remaining = self.elves
    #     active = victim = 0

    #     def inc(i: int) -> int:
    #         return (i + 1) % self.elves

    #     def next_active(active: int):
    #         active = inc(active)
    #         while not gifted[active]:
    #             active = inc(active)
    #         return active

    #     def next_victim(active: int, times: int) -> int:
    #         victim = active
    #         for _ in range(times):
    #             victim = inc(victim)
    #             while not gifted[victim]:
    #                 victim = inc(victim)
    #         return victim

    #     while remaining > 1:
    #         if remaining % 10000 == 0:
    #             print(f"Remaining {remaining}")
    #         victim = next_victim(active, remaining // 2)
    #         gifted[victim] = False
    #         remaining -= 1
    #         active = next_active(active)
    #     return active + 1

    # still too slow !
    # def gifted_elf_opposite(self) -> int:
        # print("Timer start")
        # my_timer = Timer()
        # circle = Circle(self.elves)
        # print(f"Timer elapsed {my_timer.elapsed()}")
        # # print(circle)
        # print("Timer start")
        # while circle.size > 1:
        #     if circle.size % 10000 == 0:
        #         print(f"Pending {circle.size} / Timer elapsed {my_timer.elapsed()}")
        #     circle.kill_opposite()
        #     circle.current = circle.current.following # type: ignore
        #     # print(circle)
        # print(f"Timer elapsed {my_timer.elapsed()}")
        # return circle.current.value # type: ignore

    # still to slow
    # def gifted_elf_opposite(self) -> int:
    #     print("Timer start")
    #     my_timer = Timer()
    #     elves = deque(range(1, self.elves+1))
    #     size = self.elves
    #     print(f"Timer elapsed {my_timer.elapsed()}")
    #     print("Timer start")
    #     while size > 1:
    #         if size % 50000 == 0:
    #             print(f"Pending {size} / Timer elapsed {my_timer.elapsed()}")
    #         # take me apart
    #         me = elves.popleft()
    #         half = size // 2
    #         # keep before
    #         before = deque()
    #         for _ in range(1,half):
    #             before.append(elves.popleft())
    #         # kill opponent
    #         elves.popleft()
    #         size -= 1
    #         # keep after
    #         after = deque()
    #         for _ in range(half+1, size+1):
    #             after.append((elves.popleft()))
    #         # reconstruct list for next step
    #         elves = before
    #         elves.extend(after)
    #         elves.append(me)
    #     print(f"Timer elapsed {my_timer.elapsed()}")
    #     return elves[0]

    # try reimplement who_gets_the_gifts_p2
    # still works well, but still don't understand why
    # def gifted_elf_opposite(self) -> int:
    #     def print_lr(prefix, left, right):
    #         print(f"{prefix} -> left: {left} -> right:{right}")
        
    #     half = self.elves // 2
    #     left = deque(range(1, half + 1))
    #     right = deque(range(self.elves, half, -1))
    #     affected = {
    #         True: left,
    #         False: right
    #     }
    #     # print_lr('Init', left, right)
    #     while left and right:
    #         affected[len(left) > len(right)].pop()
    #         # print_lr('pop', left, right)
    #         right.appendleft(left.popleft())
    #         left.append(right.pop())
    #         # print_lr('rot', left, right)
    #     return affected[len(left) > len(right)].pop()

    # Observed the pattern
    # took me a while to experimentd and observe, but glad I found out
    def gifted_elf_opposite(self) -> int:
        def max_pow3(size: int) -> int:
            keep = 1
            for _ in count():
                p = 3*keep
                if p > size:
                    return keep
                else:
                    keep = p
            raise ValueError('Should never happen')
        
        if self.elves < 3:
            return 1
        mp3 = max_pow3(self.elves)
        if mp3 == self.elves:
            return mp3
        remaining = self.elves - mp3
        if remaining <= mp3:
            return remaining
        return remaining + 2 * (remaining - mp3)


# quite fast btw
# def who_gets_the_gifts(elf_count: int) -> int:
#     pos = 1
#     for i in range(1, elf_count + 1):
#         if pos > i:
#             pos = 1
#         pos += 2
#     return pos - 2

# WTF: I get what it does, but not why this solves the problem / quick 1410967
# def who_gets_the_gifts_p2(elf_count: int) -> int:
#     left = deque()
#     right = deque()
#     for i in range(1, elf_count + 1):
#         if i < (elf_count // 2) + 1:
#             left.append(i)
#         else:
#             right.appendleft(i)

#     while left and right:
#         print()
#         if len(left) > len(right):
#             left.pop()
#         else:
#             right.pop()

#         # rotate
#         right.appendleft(left.popleft())
#         left.append(right.pop())
#     return left[0] or right[0]

def exo1(data: str) -> int:
    elves = int(data.strip())
    # return WhiteElephantParty(elves).gifted_elf()
    return WhiteElephantParty(elves).gifted_elf_next()
    # return who_gets_the_gifts(elves)

# << 5963999991 
def exo2(data: str) -> int:
    elves = int(data.strip())
    # for i in range(1, 200):
    #     print(f"{i} -> {WhiteElephantParty(i).gifted_elf_opposite()}")
    # return 2
    return WhiteElephantParty(elves).gifted_elf_opposite()
    # return who_gets_the_gifts_p2(elves)

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 3,
        },
        'real_data': {
            'type': 'raw',
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
        },
        'real_data': {
            'type': 'raw',
            'from': REAL_DATA_2,
        },
        'runner': exo2,
    },
)
