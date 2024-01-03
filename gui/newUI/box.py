"""
TODO: UI class that takes in disp_surf, pos_func, and size_func as init
 and has update func
TODO: separate out the box, text box, and image box classes.
 Allow a combo to be used by implementing them with composition
"""
import pygame
from .UI import UiElement
from .iterfaces import Color, Direction
from typing import Callable


X = 0
Y = 1


class Box(UiElement):
    """Box with background and boarder colors."""
    def __init__(
            self,
            display_surface: pygame.surface.Surface,
            position_function: Callable[[int, int], tuple[int, int]],
            size_function: Callable[[int, int], tuple[int, int]],
            background_color: Color = 'light gray',

            focused_color: Color = 'dark gray',

            corner_rounding_amount: int = 10,

            border_color: Color = Color('black'),
            border_size: int = 10,

            draw_from: 'Direction' = Direction.topleft,

            fill_in_border: bool = True,
    ) -> None:
        super().__init__(display_surface, position_function, size_function)
        self.background_color = background_color.color
        self.focused_color = focused_color
        self.corner_rounding_amount = corner_rounding_amount
        self.border_color = border_color.color
        self.border_size = border_size
        self.draw_from = draw_from
        self.fill_in_border = fill_in_border

    def draw(self):
        if self.hidden:
            return

        if self.draw_from == Direction.center:
            self.set_position((self.position[X] - self.size[X], self.position[Y] - self.size[Y]))

        if (self.fill_in_border and self.border_size) or not self.border_size:
            color = self.focused_color if self.is_hovered_over or self.is_selected else self.background_color
            pygame.draw.rect(self.display_surface, color, self.rect, 0, self.corner_rounding_amount)

        if self.border_size:
            pygame.draw.rect(
                self.display_surface, self.border_color, self.rect, self.border_size, self.corner_rounding_amount
            )

    def set_position(self, position: tuple[int, int]):
        self.position = position

    def move(self, displacement: tuple[int, int]):
        self.position = self.position[X] + displacement[X], self.position[Y] + displacement[Y]
