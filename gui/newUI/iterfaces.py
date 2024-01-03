from enum import Enum
from typing import overload


class Color:
    @overload
    def __init__(self): ...

    @overload
    def __init__(self, color: str): ...

    @overload
    def __init__(self, r: int, g: int, b: int): ...

    @overload
    def __init__(self, r: int, g: int, b: int, a: int): ...

    def __init__(self, *args):
        if len(args) == 0:
            self.__color = None
            return
        match args:
            case [color]: self.__color = color
            case [r, g, b]: self.__color = r, g, b
            case [r, g, b, a]: self.__color = r, g, b, a
            case default:
                raise ValueError(f"\"{default}\" is not a supported value")

    @property
    def color(self) -> tuple | str | None: return self.__color


class OverflowingOptions(Enum):
    resize_text = 0
    resize_box_down = 1
    resize_box_right = 2
    allow_overflow = 3


# noinspection SpellCheckingInspection
class Direction(Enum):
    topleft = 0
    midtop = 1
    topright = 2

    midleft = 3
    center = 4
    midright = 5

    bottomleft = 6
    midbottom = 7
    bottomright = 8
