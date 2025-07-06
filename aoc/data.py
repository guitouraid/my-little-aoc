from aoc import ReadMode
from aoc.settings import AOCSettings

class BaseData:
    def _read_all(self) -> str:
        raise NotImplementedError

    def _read_lines(self) -> list[str]:
        raise NotImplementedError

    def _read_nostrip(self) -> str:
        raise NotImplementedError

    def read(self, mode: ReadMode) -> str|list[str]:
        match mode:
            case ReadMode.READ_LINES:
                return self._read_lines()
            case ReadMode.READ_ALL:
                return self._read_all()
            case ReadMode.READ_NOSTRIP:
                return self._read_nostrip()
            case _:
                raise NotImplementedError("Invalid read mode {mode}")


class RawData(BaseData):
    def __init__(self, data: str) -> None:
        self.data = data
        super().__init__()

    def _read_nostrip(self) -> str:
        return self.data

    def _read_all(self) -> str:
        return self.data.strip()

    def _read_lines(self) -> list[str]:
        return [line.strip() for line in self._read_all().split('\n')]


class FileData(BaseData):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()

    def _read_nostrip(self) -> str:
        with open(self.path) as fd:
            return fd.read()

    def _read_all(self) -> str:
        with open(self.path) as fd:
            return fd.read().strip()

    def _read_lines(self) -> list[str]:
        return [line.strip() for line in self._read_all().splitlines()]

class DataProvider:
    def __init__(self, globals: AOCSettings, year: int, day: int) -> None:
        self.globals = globals
        self.year = year
        self.day = day

    def get_data(self, settings: dict, key: str) -> BaseData:
        ds = settings[key]
        match ds.get('type'): # type: ignore
            case 'raw':
                return RawData(ds.get('from')) # type: ignore
            case 'file':
                return FileData(
                    self.globals.get_data_path(
                        self.year,
                        self.day,
                        ds.get('from'),
                    )
                )
            case _:
                raise ValueError(f"Unsupported type: {ds.get('from')}") # type: ignore
