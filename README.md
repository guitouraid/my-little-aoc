# my-little-aoc

A quite simple `python` environment for AOC challenges

## What's in there?

A minimalistic framework that can be used to try and solve daily [AOC](https://adventofcode.com/) challenges.
Simply provides a command line program (`aoc.py`) with 2 sub commands:

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
# and go with second exercise
```

### And just a warning

If you don't want to be spoiled any solution, just avoid looking at `my-little-adventure` branch.


## How it works

When you prepare settings file for a day, you roughly generate a python file, with mostly all prefilled
to let you start with just filling in the functions to solve exercise 1 and 2.
Let's check and see how it looks like.

### Read mode and data

File starts with a few definitions, for read mode and data.

Two read modes are available for data
- all: the whole as a string
- lines: a list of lines

And since the latter is often the most convenient, simple and stupid:

```python
READ_MODE = "lines"
```

For data, most of the time, test data fits well in place while it is as easy to save daily input in a convenient place.
And most of the time, same data applies for both exercises.

```python
TEST_DATA_2 = TEST_DATA_1 = """
2x3x4
1x1x10
"""

### store file under `DATA_DIR`
REAL_FILE_2 = REAL_FILE_1 = "2015_2.txt"
```

### The 2 functions skeletons

Nothing much to say...

```python
def exo1(data: list[str]) -> int:
    return 0

def exo2(data: list[str]) -> int:
    return 0
```

### and last the actual settings variable

This is what will be loaded from our program to run the exercises.
It comes in the form of a `tuple` of `dict`, each containing definitions required for one exercise:
- the runner: the function that will be executed
- the read mode: `READ_MODE` should be OK
- the test and real data specs:
    - type: 'raw' for test data and 'file' for real should do it
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

## How to customize for your need

You could first replace the [default template](aoc/templates/settings.py.j2) with your own. As long s you provide
a `dict` named `settings` with a structure similar to the [default one](aoc/templates/settings.py.j2), it should work.
And all you have to know is that template variables are `year`, `day`, `read` (read mode can be `all` for raw string or `lines` for a list of stripped lines) and `input` (input mod can be `raw` for raw string data or `file` for file name).
The rest is at your discretion.

For example: `my_custom_template.py.j2`

```
READ_MODE = "{{ read.value }}"
TEST_DATA = "" # TODO: fill in with sample data
REAL_FILE = "input" # TODO: store input file

def first(data):
    # TODO: complete function

def second(data):
    # TODO: complete function

settings = (
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA,
            'expected': None, # TODO: set expected test value
            # 'kw_args': {},
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE,
            # 'kw_args': {},
        },
        'runner': first,
    },
    {
        'read_mode': READ_MODE,
        'test_data': {
            'type': 'raw',
            'from': TEST_DATA,
            'expected': None, # TODO: set expected test value
            # 'kw_args': {},
        },
        'real_data': {
            'type': 'file',
            'from': REAL_FILE,
            # 'kw_args': {},
        },
        'runner': second,
    },
)


```

Now, imagine you want to organize with exercise and 'input' file in the same place (smth like `_2015/02/{day02.py,input}`),
the only requirement is that exercises must be placed under `settings` directory.
Then you could create a `.env` file with the following content:

```
SETTINGS_DIR='_{year}/{day:02d}'
DATA_DIR='settings/_{year}/{day:02d}'
SETTINGS_FILE='day{day:02d}.py'
TEMPLATE='my_custom_template.py.j2'
```
... and make your own template (if not already done).

Note: you might also want to change default read mode for template in `.env` file (`READ_MODE='all'`),
or you might agree it makes quite a good default...
Alternatively, the `prepare` sub command has a `read` option if you guess a specific exercise will require changing and
you can always directly change it in your generated exercise file (just take care not to put an invalid value).


## What if?..

### What if you don't get the point about `kw_args` ?

Well, happens to be usefull just on rare occasions...
For example, sometimes an exercise need to perform an operation a certain number of times, that differ between test and real solution.
Then just make your exercise function take another argument `def exo1(data, rounds)`
and add in settings where relevant `'kwargs': {'rounds': X}`

### What if any question would reach my mind or one would ask some ?

I bet I would complete the current section
