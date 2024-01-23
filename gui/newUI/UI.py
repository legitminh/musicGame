"""
TODO: children and parrents
"""
from copy import copy
import pygame
from typing import Any, Callable, Union
from abc import abstractmethod, ABC


class UiElement(ABC):
    is_selected: bool = False
    hidden: bool = False

    def __init__(
            self,
            display_surface: pygame.surface.Surface,
            position_function: Callable[[int, int], tuple[int, int]],
            size_function: Callable[[int, int], tuple[int, int]],
    ) -> None:
        self.display_surface = display_surface
        self.display_size = display_surface.get_size()

        self.dx, self.dy = 0, 0
        self.position_function = lambda x, y: (
            position_function(x, y)[0] + self.dx, position_function(x, y)[1] + self.dy
        )
        self.size_function = lambda x, y: (
            size_function(x, y)[0], size_function(x, y)[1]
        )

        self.position = self.position_function(*self.display_size)
        self.size = self.size_function(*self.display_size)

        self.rect = pygame.rect.Rect(self.position, self.size)

    def update(self, event: pygame.event.Event) -> Any:
        if event.type == pygame.VIDEORESIZE:
            self.display_size = self.display_surface.get_size()


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self.is_selected = self.is_hovered_over ^ self.is_selected & self.is_hovered_over

    def set_pos_func(self, pos_func: Callable[[int, int], tuple[int, int]]) -> 'UiElement':
        tmp = copy(self)
        tmp.position_function = pos_func
        tmp.dx, tmp.dy = 0, 0
        return tmp

    def set_size_func(self, size_func: Callable[[int, int], tuple[int, int]]) -> 'UiElement':
        tmp = copy(self)
        tmp.size_function = size_func
        tmp.dx, tmp.dy = 0, 0
        return tmp
    
    def update_position(self):
        self.position = self.position_function(*self.display_size)
        self.size = self.size_function(*self.display_size)
        self.rect = pygame.rect.Rect(self.position, self.size)

    def set_position(self, position: tuple[int, int]) -> None:
        pos = self.position
        self.dx += position[0] - pos[0]
        self.dy += position[1] - pos[1]
        self.update_position()

    def move(self, vector: tuple[int, int]) -> None:
        self.dx, self.dy = vector

    @property
    def is_hovered_over(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @abstractmethod
    def draw(self): ...

    @staticmethod
    def is_attribute(attr) -> bool:
        try:
            getattr(UiElement, attr)
            return True
        except AttributeError:
            return False

    @staticmethod
    def set_default(**kwargs):
        for arg, _ in kwargs.items():
            if not UiElement.is_attribute(arg):
                raise ValueError(f"\"{arg}\" is not an attribute of a UI element")

        for arg, val in kwargs.items():
            UiElement.__setattr__(UiElement, arg, val)
    
    @property
    def top(self): return self.rect.top
    
    @property
    def bottom(self): return self.rect.bottom
    
    @property
    def left(self): return self.rect.left
    
    @property
    def right(self): return self.rect.right

    @property
    def height(self): return self.rect.height
    
    @property
    def width(self): return self.rect.width
    
    @property
    def topleft(self): return self.rect.topleft

    @property
    def topright(self): return self.rect.topright

    @property
    def bottomleft(self): return self.rect.bottomleft

    @property
    def bottomright(self): return self.rect.bottomright


class UiElementGroup:
    def __init__(self, *args: Union[UiElement, 'UiElementGroup']):
        self.elements = args

    def update(self, event: pygame.event.Event):
        [element.update(event) for element in self.elements]

    def draw(self):
        [element.draw() for element in self.elements]

    def move(self):
        [element.move() for element in self.elements]
    
    @property
    def top(self): return min(element.top for element in self.elements)

    @property
    def bottom(self): return max(element.bottom for element in self.elements)

    @property
    def left(self): return min(element.left for element in self.elements)

    @property
    def right(self): return max(element.right for element in self.elements)

    @property
    def height(self): return self.bottom - self.top
    
    @property
    def width(self): return self.right - self.left

    @property
    def topleft(self): return (self.left, self.top)

    @property
    def topright(self): return (self.right, self.top)

    @property
    def bottomleft(self): return (self.left, self.bottom)

    @property
    def bottomright(self): return (self.right, self.bottom)
