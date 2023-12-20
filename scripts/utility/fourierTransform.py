#Change mp3 to frequencies vs list[tuple]
from enum import Enum
from typing import NewType


class Note(Enum):
    a = 1
    b = 2
    c = 3
    d = 4


Duration = NewType("Duration", float)

output: list[list[tuple[Duration, Note], ], ]
