#!/bin/env python

import importlib
import os
from pathlib import Path
from typing_extensions import Annotated
import typer
from jinja2 import Environment, PackageLoader, select_autoescape

from aoc import InputType, ReadMode
from aoc.exercise import Exercise
from aoc.settings import AOCSettings


year_type = Annotated[int, typer.Argument(help="Which year ?")]
day_type = Annotated[int, typer.Argument(help="Which day ?")]

app = typer.Typer(help="Yeah, it's Advent of Code !")
globals = AOCSettings.from_env(os.path.dirname(__file__))

@app.command()
def prepare(
        year: year_type,
        day: day_type,
        replace: Annotated[bool, typer.Option(help="Replace existing")] = False,
        read: Annotated[ReadMode, typer.Option(help="Set read mode")] = globals.read_mode,
        input: Annotated[InputType, typer.Option(help='Set input type')] = globals.input_type,
        template: Annotated[str, typer.Option(help='Use template file')] = globals.template,
    ):
    """
    Oh, yet another Advent of Code day !
    """
    base = globals.get_settings_base()
    for t in globals.get_settings_dir(year, day).split('/'):
        target = os.path.join(base, t)
        if not os.path.exists(target):
            os.mkdir(target)
            Path.touch(os.path.join(target, '__init__.py')) # type: ignore
            base = target
    try:
        target = open(globals.get_settings_path(year, day), 'w' if replace else 'x')
    except FileExistsError:
        print("Use `--replace` option to overwrite")
        raise typer.Exit()
    tmpl_env = Environment(
        loader=PackageLoader("aoc"),
        autoescape=select_autoescape()
    )
    tmpl = tmpl_env.get_template(template)
    target.write(tmpl.render(year=year, day=day, read=read, input=input))
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
    imp_mod = importlib.import_module(globals.get_settings_mod(year, day))
    settings = getattr(imp_mod, "settings")
    exercise = Exercise.from_settings(globals, settings[exo-1], year, day)
    exercise.run(test)

if __name__ == '__main__':
    app()
