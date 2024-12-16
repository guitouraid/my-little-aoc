#!/bin/env python

import importlib
import os
from pathlib import Path
from typing_extensions import Annotated
import typer
from jinja2 import Environment, PackageLoader, select_autoescape

from aoc import Exercise

DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    'data'
)

year_type = Annotated[int, typer.Argument(help="Which year ?")]
day_type = Annotated[int, typer.Argument(help="Which day ?")]

app = typer.Typer(help="Yeah, it's Advent of Code !")

@app.command()
def prepare(
        year: year_type,
        day: day_type,
        replace: Annotated[bool|None, typer.Option(help="Replace existing")] = False,
    ):
    """
    Oh, yet another Advent of Code day !
    """
    target_paths = [os.path.dirname(__file__), 'settings', f'{year}', f'settings_{year}_{day}.py']
    target_path = os.path.join(*target_paths[:-1])
    if not os.path.exists(target_path):
        os.mkdir(target_path)
        Path.touch(os.path.join(target_path, '__init__.py')) # type: ignore
    target_path = os.path.join(*target_paths)
    try:
        target = open(target_path, 'w' if replace else 'x')
    except FileExistsError:
        print("Use `--replace` option to overwrite")
        raise typer.Exit()
    env = Environment(
        loader=PackageLoader("aoc"),
        autoescape=select_autoescape()
    )
    template = env.get_template("settings.py.j2")
    target.write(template.render(year=year, day=day))
    target.close()



@app.command()
def play(
        year: year_type,
        day: day_type,
        exo: Annotated[int, typer.Argument(min=1, max=2, help="Exercise 1 or 2 ?")],
        test: Annotated[bool, typer.Option(help="Run test case")] = False,
    ):
    """
    Well, let's play Advent of Code today !
    """
    imp_mod = importlib.import_module(f"settings.{year}.settings_{year}_{day}")
    settings = getattr(imp_mod, "settings")
    exercise = Exercise.from_settings(settings[exo-1]|{'data_path': os.path.join(DATA_DIR, f"{year}")})
    exercise.run(test)

if __name__ == '__main__':
    app()
