"""
A scroll bar which is composed of four boxes
1. the scrolling bar
2. the background box (optional)
3. the up arrow box (optional)
4. the down arrow box (optional)
"""


from UI import UiElement, UiElementGroup
from box import Box
from textBox import TextBox
import pygame
from enum import Enum
from typing import Callable


X = 0
Y = 1


class Orientation(Enum):
    horizontal = 0
    vertical = 1


class ScrollBar(UiElement):
    def __init__(
            self, 
            background_box: Box, 
            foreground_box: TextBox, 
            effected_group: UiElementGroup,
            display_area_func: Callable[[float, float], float],
            display_percentage: bool = False
        ) -> None:
        super().__init__(background_box.display_surface, background_box.position_function, background_box.size_function)

        self.rect = background_box.rect
        self.effected_group = effected_group
        self.display_area_function = display_area_func
        self.display_area = self.display_area_function(*self.display_surface.get_size())

        self.scroll_amount = self.effected_group.height / self.display_area / 5

        self.background_box = background_box
        if background_box.rect.width > background_box.rect.height:
            self.orientation = Orientation.horizontal
        else:
            self.orientation = Orientation.vertical

        self.foreground_box = foreground_box
        self.display_percentage = display_percentage

    def update(self, event: pygame.event.Event) -> float:
        super().update(event)
        if event.type == pygame.VIDEORESIZE:
            self.display_area = self.display_area_function(*self.display_surface.get_size())

        self.background_box.update(event)
        self.foreground_box.update(event)
        
        displacement = [0, 0]
        displacement[0 if self.orientation == Orientation.horizontal else 1] = \
            (self.effected_group.height - self.display_area) * self.foreground_box_relative_position
        self.effected_group.set_displacement(displacement)
        
        self.drag_foreground_box(event)

        return self.foreground_box_relative_position

    @property
    def foreground_box_relative_position(self):
        if self.orientation == Orientation.vertical:
            percentage = (self.background_box.rect.top - self.foreground_box.rect.top) / \
                         (self.background_box.rect.height - self.foreground_box.rect.height)
        else:
            percentage = (self.background_box.rect.left - self.foreground_box.rect.left) / \
                         (self.background_box.rect.width - self.foreground_box.rect.width)

        return percentage

    def drag_foreground_box(self, event):
        if self.background_box.is_selected:
            self.set_foreground_box_position(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            set_to = None

            if event.button == pygame.BUTTON_LEFT:
                if not self.foreground_box.is_hovered_over and self.background_box.is_selected:
                    set_to = pygame.mouse.get_pos()

            if event.button == 4:  # scroll up
                displacement = [0, 0]
                displacement[0 if self.orientation == Orientation.horizontal else 1] = -self.scroll_amount
                self.foreground_box.move(displacement)
                if self.foreground_box.top < self.background_box.top:
                    self.foreground_box.set_position(self.background_box.topleft)

            if event.button == 5:
                displacement = [0, 0]
                displacement[0 if self.orientation == Orientation.horizontal else 1] = self.scroll_amount
                self.foreground_box.move(displacement)
                if self.foreground_box.bottom > self.background_box.bottom:
                    self.foreground_box.set_position((self.background_box.left, self.background_box.bottom - self.foreground_box.height))

            if set_to is not None:
                self.set_foreground_box_position(set_to)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.background_box.is_selected = False
                self.foreground_box.is_selected = False

    def set_foreground_box_position(self, position: tuple[int, int]):
        new_pos = None
        if self.orientation == Orientation.vertical:
            if self.background_box.bottom < position[Y] + self.foreground_box.height / 2:
                new_pos = (self.foreground_box.rect.left, self.background_box.bottom - self.foreground_box.height)
            elif self.background_box.top > position[Y] - self.foreground_box.height / 2:
                new_pos = (self.foreground_box.rect.left, self.background_box.top)
            else:
                new_pos = (self.foreground_box.rect.left, position[Y] - self.foreground_box.height / 2)
        else:
            if self.background_box.left < position[X] - self.foreground_box.width / 2:
                new_pos = (self.background_box.left, self.foreground_box.rect.top)
            elif position[X] + self.foreground_box.width / 2 < self.background_box.right:
                new_pos = (self.background_box.right - self.foreground_box.width, self.foreground_box.rect.top)
            else:
                new_pos = (position[X] - self.foreground_box.width / 2, self.foreground_box.top)

        if new_pos is not None:
            self.foreground_box.set_position(new_pos)

    def draw(self):
        if self.hidden:
            return
        self.background_box.draw()
        self.foreground_box.draw()


class ScrollBarWithButtons(ScrollBar):
    pass
