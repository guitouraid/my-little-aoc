from dataclasses import dataclass
import os

from dotenv import load_dotenv
from aoc import ReadMode
from settings import DEFAULT_DATA_DIR, DEFAULT_DATA_FILE, DEFAULT_READ_MODE, DEFAULT_SETTINGS_DIR, DEFAULT_SETTINGS_FILE, DEFAULT_TEMPLATE

@dataclass
class AOCSettings:
    base: str
    data_dir: str
    settings_dir: str
    settings_file: str
    template: str
    read_mode: ReadMode

    @classmethod
    def from_env(cls, base: str):
        load_dotenv(os.path.abspath(os.path.join(
            base,
            '.env'
        )))
        return cls(
            base = base,
            data_dir = os.getenv('DATA_DIR', DEFAULT_DATA_DIR),
            settings_dir = os.getenv('SETTINGS_DIR', DEFAULT_SETTINGS_DIR),
            settings_file= os.getenv('SETTINGS_FILE', DEFAULT_SETTINGS_FILE),
            template = os.getenv('TEMPLATE', DEFAULT_TEMPLATE),
            read_mode = ReadMode(os.getenv('READ_MODE', DEFAULT_READ_MODE)), 
        )

    def get_data_path(self, year: int, day: int, data_file: str) -> str:
        """return full path to data file"""
        return os.path.abspath(os.path.join(
            self.base,
            self.data_dir.format(year=year, day=day),
            data_file.format(year=year, day=day)
        ))

    def get_settings_base(self) -> str:
        return os.path.abspath(os.path.join(
            self.base,
            'settings'
        ))

    def get_settings_dir(self, year: int, day: int) -> str:
        return self.settings_dir.format(year=year, day=day)

    def get_settings_file(self, year: int, day: int) -> str:
        return self.settings_file.format(year=year, day=day)

    def get_settings_path(self, year: int, day: int) -> str:
        """return full path to settings file"""
        return os.path.abspath(os.path.join(
            self.get_settings_base(),
            self.get_settings_dir(year, day),
            self.get_settings_file(year, day)
        ))

    def get_settings_mod(self, year: int, day: int) -> str:
        return '.'.join(
            ['settings'] +
            self.get_settings_dir(year, day).split('/') +
            [self.get_settings_file(year, day)[:-3]]
        )
