from collections.abc import Callable
from typing import Any

from aoc import ReadMode
from aoc.data import BaseData, DataProvider
from aoc.settings import AOCSettings


class Exercise:
    def __init__(self, globals: AOCSettings, runner: Callable, read_mode: ReadMode, real_data: BaseData, real_kw_args: dict|None, test_data: BaseData, test_kw_args: dict|None, test_result: Any) -> None:
        self.runner = runner
        self.read_mode = read_mode
        self.data = ((real_data, real_kw_args), (test_data, test_kw_args))
        self.test_result = test_result
        self.kw_args = (real_kw_args, test_kw_args)

    def run(self, test: bool) -> Any:
        data, kw_args = self.data[test]
        if kw_args:
            result = self.runner(data.read(self.read_mode), **kw_args)
        else:
            result = self.runner(data.read(self.read_mode))
        print(f'Result: {result}')
        if test:
            assert result == self.test_result, f"Got: {result} / Expected: {self.test_result}"

    @classmethod
    def from_settings(cls, globals: AOCSettings, settings: dict, year: int, day: int):
        dp = DataProvider(globals, year, day)
        runner = settings.get('runner')
        # in case one would type 0 or 1
        read_mode = ReadMode(settings.get('read_mode'))
        real_set = settings.get('real_data')
        real_kw = real_set.get('kw_args') # type: ignore
        real_data = dp.get_data(settings, 'real_data')
        test_set = settings.get('test_data')
        test_kw = test_set.get('kw_args') # type: ignore
        test_data = dp.get_data(settings, 'test_data')
        test_result = test_set.get('expected') # type: ignore
        return cls(globals, runner, read_mode, real_data, real_kw, test_data, test_kw, test_result) # type: ignore
