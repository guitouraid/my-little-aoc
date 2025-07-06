from enum import Enum

class ReadMode(str, Enum):
    READ_LINES = "lines"
    READ_ALL = "all"
    READ_NOSTRIP = "nostrip"

    @property
    def data_type(self):
        match self:
            case ReadMode.READ_LINES:
                return 'list[str]'
            case ReadMode.READ_ALL|ReadMode.READ_NOSTRIP:
                return 'str'

class InputType(str, Enum):
    FILE = "file"
    RAW = 'raw'

class OutputType(str, Enum):
    INT = 'int'
    STR = 'str'

    @property
    def sample(self) -> str:
        match self:
            case OutputType.INT:
                return '0'
            case OutputType.STR:
                return "''"
