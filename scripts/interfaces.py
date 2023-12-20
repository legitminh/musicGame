from typing import Callable
from enum import Enum


class ExitException(Exception):
    """
    Error raised when the Player exits the screen
    """
    pass


class Screens(Enum):
    intro = 1
    menu = 2
    leveOptions = 3
    level = 4
    outro = 5
    option = 6

parameters = str | int | float
mode_type = tuple[Screens, dict[str, parameters]]
