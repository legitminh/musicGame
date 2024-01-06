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


X = 0
Y = 1


class Orientation(Enum):
    horizontal = 0
    vertical = 1


class ScrollBar(UiElement):
    is_being_dragged = False

    def __init__(
            self, 
            background_box: Box, 
            foreground_box: TextBox, 
            effected_group: UiElementGroup,
            display_area: float,
            display_percentage: bool = False
        ) -> None:
        super().__init__(background_box.display_surface, background_box.position_function, background_box.size_function)

        self.rect = background_box.rect
        self.effected_group = effected_group
        self.display_area = display_area

        self.scroll_amount = self.effected_group.height / self.display_area

        self.background_box = background_box
        if background_box.rect.width > background_box.rect.height:
            self.orientation = Orientation.horizontal
        else:
            self.orientation = Orientation.vertical

        self.foreground_box = foreground_box
        self.display_percentage = display_percentage

    def update(self, event: pygame.event.Event) -> float:
        self.drag_foreground_box(event)

        self.background_box.update(event)
        if self.background_box.rect is not self.rect:
            self.rect = self.background_box.rect
        self.foreground_box.update(event)
        self.effected_group
        super().update(event)

        return self.find_foreground_box_relative_position

    @property
    def find_foreground_box_relative_position(self):
        if self.orientation == Orientation.vertical:
            percentage = (self.background_box.rect.top - self.foreground_box.rect.top) / \
                         (self.background_box.rect.height - self.foreground_box.rect.height)
        else:
            percentage = (self.background_box.rect.left - self.foreground_box.rect.left) / \
                         (self.background_box.rect.width - self.foreground_box.rect.width)

        return percentage

    def drag_foreground_box(self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            set_to = self.foreground_box.position

            if event.button == pygame.BUTTON_LEFT:
                if self.foreground_box.is_selected:
                    self.is_being_dragged = True

                if not self.foreground_box.is_hovered_over or self.is_being_dragged:
                    set_to = pygame.mouse.get_pos()

            if event.button == pygame.MOUSEBUTTONDOWN:
                set_to = pygame.mouse.get_pos()[0] - self.scroll_amount, pygame.mouse.get_pos()[1] - self.scroll_amount

            if event.button == pygame.MOUSEBUTTONUP:
                set_to = pygame.mouse.get_pos()[0] + self.scroll_amount, pygame.mouse.get_pos()[1] + self.scroll_amount

            self.set_foreground_box_position(set_to)

        elif event == pygame.MOUSEBUTTONUP:
            if event.button != pygame.BUTTON_LEFT:
                self.is_being_dragged = False
                self.foreground_box.is_selected = False

    def set_foreground_box_position(self, position: tuple[int, int]):
        if self.orientation == Orientation.vertical:
            new_position = (self.foreground_box.rect.left, position[Y])
        else:
            new_position = (position[X], self.foreground_box.rect.top)

        self.foreground_box.set_position(new_position)

    def draw(self):
        if self.hidden:
            return
        self.background_box.draw()
        self.foreground_box.draw()


class ScrollBarWithButtons(ScrollBar):
    pass
