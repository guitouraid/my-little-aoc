# my-little-aoc

A quite simple `python` environment for AOC challenges

## What's in there?

A minimalistic framework that can be used to try and solve daily [AOC](https://adventofcode.com/) challenges.
Simply provides a command line program (`aoc.py`) with 2 commands:

- `prepare`: generate a settings file for specific day

- `play`: to run a specific exercise


## Getting started

Prerequisite is `python3` installed, obviously (with `pip` module too)

### Set up a virtual environment

For example using `venv`

```sh
# create a virtual environment named `aoc`
python -m venv --prompt aoc .venv
# and activate
source .venv/bin/activate
```

### Install the few requirements

```sh
pip install -r requirements.txt 
```

### Enjoy the day

Supposed you would want to start from the early days

```sh
# generate the settings file
./aoc.py prepare 2015 1
# Use your favourite editor/IDE and fill in some settings and the `exo_1` function, for a start
# Then try your solution against testing data
./aoc.py play 2015 1 1 --test
# and when confident enough
./aoc.py play 2015 1 1
# Now you can copy/paste the solution on [AOC](https://adventofcode.com/) to reclaim your first star
```

### And just a warning

If you don't want to be spoiled any solution, just avoid looking at `my-little-adventure` branch.


## A little more about the environment

When you prepare settings file for a day, you roughly generate a python file, with mostly all prefilled
to let you start with just filling in the functions to solve exercise 1 and 2.
Let's check and see how it looks like.

### Read mode and data

After imports, file starts with a few definitions, for read mode and data.

Two read modes are available for data, the whole as a string, or a list of lines.
And since the latter is often the most convenient, simple and stupid:

```python
READ_MODE = ReadMode.READ_LINES
#READ_MODE = ReadMode.READ_ALL
```

For data, most of the time, test data fits well in place while it is as easy to save daily input in a convenient place.
And most of the time, same data applies for both exercises.

```python
TEST_DATA_2 = TEST_DATA_1 = """
2x3x4
1x1x10
"""

### store file in `data/2015` dir
REAL_FILE_2 = REAL_FILE_1 = "2015_2_1.txt"
```

### The 2 functions skeletons

Nothing much to say... One might object about the `Any` return type
But if I prefer int, some might prefer string for their own reasons, or even be imaginative...

```python
def exo1(data: list[str]|str) -> Any:
    pass

def exo2(data: list[str]|str) -> Any:
    pass
```

### and last the actual settings variable

This is what will be loaded from our program to run the exercises.
It comes in the form of a `tuple` of `dict`, each containing definitions required for one exercise:
- the runner: the function that will be executed
- the read mode: `READ_MODE` should be OK
- the test and real data specs:
    - type: 'raw' for test data and 'file' for real shoulld do it
    - from: `{TEST,REAL}_DATA_{1,2}` relying on previous definitions
    - expected: only for test ! To be replaced with the expected return value
    - kw_args: optional, a dict to be passed as keyword arguments to the runner

```python
settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA_1,
            'expected': 101,
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
            'expected': 48,
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE_2,
        },
        'runner': exo2,
    },
)
```

## What if?..

### What if you would prefer another organization for my data ?

Right now, you may just change value for the datapath, directly in generated file or the template.
Playing with absolute or relative paths, you should get your way to your input file.

### What if other questions would reach my mind ?

I bet I would complete the current section
