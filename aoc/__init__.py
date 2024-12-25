from enum import Enum

class ReadMode(str, Enum):
    READ_LINES = "lines"
    READ_ALL = "all"

    def data_type(self):
        match self:
            case ReadMode.READ_LINES:
                return 'list[str]'
            case ReadMode.READ_ALL:
                return 'str'
