from copy import copy
import pygame
from typing import Any, Callable, Union
from abc import abstractmethod, ABC




class UiElement(ABC):
    is_selected: bool = True
    hidden: bool = False
    stored_value = None

    def __init__(
            self,
            display_surface: pygame.surface.Surface,
            position_function: Callable[[int, int], tuple[int, int]],
            size_function: Callable[[int, int], tuple[int, int]]
    ) -> None:
        self.display_surface = display_surface
        self.display_size = display_surface.get_size()

        self.position_function = position_function
        self.size_function = size_function

        self.position = self.position_function(*self.display_size)
        self.size = self.size_function(*self.display_size)

        self.rect = pygame.rect.Rect(self.position, self.size)

    def update(self, event: pygame.event.Event) -> Any:
        if event.type == pygame.VIDEORESIZE:
            self.display_size = self.display_surface.get_size()

            self.position = self.position_function(*self.display_size)
            self.size = self.size_function(*self.display_size)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self.is_selected = self.is_hovered_over ^ self.is_selected & self.is_hovered_over

        self.draw()

    def set_pos_func(self, pos_func: Callable[[int, int], tuple[int, int]]) -> 'UiElement':
        tmp = copy(self)
        tmp.position_function = pos_func
        return tmp

    def set_size_func(self, size_func: Callable[[int, int], tuple[int, int]]) -> 'UiElement':
        tmp = copy(self)
        tmp.size_function = size_func
        return tmp

    @property
    def is_hovered_over(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @abstractmethod
    def draw(self): ...

    def store(self, value):
        self.stored_value = value

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


class UiElementGroup:
    def __init__(self, *args: Union[UiElement, 'UiElementGroup']):
        self.elements = args

    def update(self, event: pygame.event.Event):
        for element in self.elements:
            element.update(event)

    def draw(self):
        for event in self.elements:
            event.draw()
