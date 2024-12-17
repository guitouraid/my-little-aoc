from typing import Any
from aoc import ReadMode


### all at once or line by line?
READ_MODE = ReadMode.READ_LINES

### test/real data as raw string or file
TEST_DATA_2 = TEST_DATA_1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

### store file in `data` dir
REAL_FILE_2 = REAL_FILE_1 = "2024_4_1.txt"

def find_char(data: list[str], char: str) -> list[tuple[int, int]]:
    xs = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == char:
                xs.append((i,j))
    return xs

def find_xmas(data: list[str], line, idx) -> int:
    WORD="XMAS"
    height = len(data)
    width = len(data[0])
    L = R = U = D = LU = LD = RU = RD = 1
    for i in range(1, len(WORD)):
        stop_l = idx -i < 0
        stop_r = idx + i >= width
        stop_u = line - i < 0
        stop_d = line + i >= height
        if L:
            if stop_l or data[line][idx-i] != WORD[i]:
                L = 0
        if R:
            if stop_r or data[line][idx+i] != WORD[i]:
                R = 0
        if U:
            if stop_u or data[line-i][idx] != WORD[i]:
                U = 0
        if D:
            if stop_d or data[line+i][idx] != WORD[i]:
                D = 0
        if LU:
            if stop_l or stop_u or data[line-i][idx-i] != WORD[i]:
                LU = 0
        if LD:
            if stop_l or stop_d or data[line+i][idx-i] != WORD[i]:
                LD = 0
        if RU:
            if stop_r or stop_u or data[line-i][idx+i] != WORD[i]:
                RU = 0
        if RD:
            if stop_r or stop_d or data[line+i][idx+i] != WORD[i]:
                RD = 0
    return L + R + U + D + LU + LD + RU + RD

def find_mas(data: list[str], line, idx) -> int:
    height = len(data)
    width = len(data[0])
    if line == 0 or line == height-1 or idx == 0 or idx == width-1:
        return 0
    WORD="MAS"
    M = WORD[0]
    S = WORD[-1]
    ul = data[line-1][idx-1]
    ur = data[line-1][idx+1]
    dl = data[line+1][idx-1]
    dr = data[line+1][idx+1]
    if ((ul == M and dr == S) or (ul == S and dr == M)) and ((ur == M and dl == S) or (ur == S and dl == M)):
        return 1
    return 0



def exo1(data: list[str]) -> Any:
    return sum([find_xmas(data, line, idx) for line, idx in find_char(data, "X")])

def exo2(data: list[str]) -> Any:
    return sum([find_mas(data, line, idx) for line, idx in find_char(data, "A")])

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 18,
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
            'expected': 9,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)