from enum import Enum


# https://docs.python.org/3/library/enum.html
class LineStatus(Enum):
    ParsedSuccessfully = 1
    Corrupted = 2
    Incomplete = 3
