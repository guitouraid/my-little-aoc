from collections.abc import Callable
from enum import Enum
import os
from typing import Any

class ReadMode(Enum):
    READ_LINES = 0
    READ_ALL = 1

class BaseData:
    def _read_all(self) -> str:
        raise NotImplementedError

    def _read_lines(self) -> list[str]:
        raise NotImplementedError

    def read(self, mode: ReadMode) -> str|list[str]:
        match mode:
            case ReadMode.READ_LINES:
                return self._read_lines()
            case ReadMode.READ_ALL:
                return self._read_all()
            case _:
                raise NotImplementedError("Invalid read mode {mode}")


class RawData(BaseData):
    def __init__(self, data: str) -> None:
        self.data = data
        super().__init__()

    def _read_all(self) -> str:
        return self.data

    def _read_lines(self) -> list[str]:
        return [line.strip() for line in self.data.strip().split('\n')]


class FileData(BaseData):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()

    def _read_all(self) -> str:
        with open(self.path) as fd:
            return fd.read()

    def _read_lines(self) -> list[str]:
        with open(self.path, buffering=1) as fd:
            return [line.strip() for line in fd if line]
 

class Exercise:
    def __init__(self, runner: Callable, read_mode: ReadMode, real_data: BaseData, real_kw_args: dict|None, test_data: BaseData, test_kw_args: dict|None, test_result: Any) -> None:
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
    def from_settings(cls, settings: dict):
        runner = settings.get('runner')
        # in case one would type 0 or 1
        read_mode = ReadMode(settings.get('read_mode'))
        real_set = settings.get('real_data')
        real_kw = real_set.get('kw_args') # type: ignore
        match real_set.get('type'): # type: ignore
            case 'raw':
                real_data = RawData(real_set.get('from')) # type: ignore
            case 'file':
                real_data = FileData(os.path.join(settings.get('data_path'), real_set.get('from'))) # type: ignore
            case _:
                raise ValueError(f"Unsupported type: {real_set.get('from')}") # type: ignore
        test_set = settings.get('test_data')
        test_kw = test_set.get('kw_args') # type: ignore
        match test_set.get('type'): # type: ignore
            case 'raw':
                test_data = RawData(test_set.get('from')) # type: ignore
            case 'file':
                test_data = FileData(os.path.join(settings.get('data_path'), test_set.get('from'))) # type: ignore
            case _:
                raise ValueError(f"Unsupported type: {test_set.get('from')}") # type: ignore
        test_result = test_set.get('expected') # type: ignore
        return cls(runner, read_mode, real_data, real_kw, test_data, test_kw, test_result) # type: ignore
