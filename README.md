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

TODO: bring in some more stuff (details about settings file, other?..)
