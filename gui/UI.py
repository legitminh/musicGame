"""
TODO: correct the scroll bar calculation
"""


import pygame
from enum import Enum
from constants import *
from typing import Any, Callable


class Button(pygame.sprite.Sprite):
    # the center of the button, text, color of sprite, color of text, image path, dimensions (if there is an image path)
    def __init__(self,
                 surface,
                 pos: tuple[int | float] | list[int | float],
                 mode_c: Any,
                 text=None,
                 text_size=None, *,
                 color=(150, 150, 150),
                 text_color='black',
                 path='',
                 dim=(),
                 alpha=255,
                 alignment_pos='center') -> None:
        """
        :param pos: The position of the center of the button
        :param mode_c: When clicked, the button will return this parameter
        :param text: The text the button will display (text is the size of the button)
        :param text_size: The size of the text the button displays (controls the size of the button)
        :param color: The color of the background of the button
        :param text_color: The color of the text the button displays
        :param path: The image path
        :param dim: The size of the image
        :param alpha: The alpha value of alpha
        """
        super().__init__()
        self.surface, self.pos, self.text, self.color, self.text_color, self.mode_c, self.ts, self.alignment = \
            surface, pos, text, color, text_color, mode_c, text_size, alignment_pos
        if (text or text == 0) and path:
            self.rect = pygame.font.Font(FONT_PATH, self.ts).render(
                str(self.text), True, self.text_color).get_rect()
            self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                                dim)  # resizes the image to 'dim'
            self.rect = self.image.get_rect()
        elif text or text == 0:  # needs to have 'text' and 'text_size'
            self.rect = pygame.font.Font(FONT_PATH, self.ts).render(
                str(text), True, self.text_color).get_rect()
            dim = self.rect.bottomright[0] - self.rect.topleft[0] + 20, self.rect.bottomright[1] - self.rect.topleft[
                1] + 20
            self.image = pygame.Surface(dim, pygame.SRCALPHA).convert_alpha()
            self.image.fill((color[0], color[1], color[2], alpha))
            self.rect = self.image.get_rect()
        else:  # needs to have 'path' and 'dim'
            self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(),
                                                dim)  # resizes the image to 'dim'
            self.rect = self.image.get_rect()
        self.set_pos(self.pos)

    def update(self) -> None:
        text = pygame.font.Font(FONT_PATH, self.ts).render(str(self.text), True, self.text_color)
        self.surface.blit(text, text.get_rect(center=self.rect.center))

    def color_changer(self, color) -> None:
        self.image.fill(color)

    def set_pos(self, pos):
        self.pos = tuple(pos)
        if self.alignment == 'center':
            self.rect.center = self.pos
        elif self.alignment == 'topleft':
            self.rect.topleft = self.pos
        elif self.alignment == 'topright':
            self.rect.topright = self.pos
        elif self.alignment == 'bottomleft':
            self.rect.bottomleft = self.pos
        elif self.alignment == 'bottomright':
            self.rect.bottomright = self.pos


class AlignmentTypes(Enum):
    center, c = 0, 0

    # corners
    topleft, tl = 1, 1
    topright, tr = 2, 2
    bottomleft, bl = 3, 3
    bottomright, br = 4, 4

    # center of sides
    midtop, mt = 5, 5
    midbottom, mb = 6, 6
    midleft, ml = 7, 7
    midright, mr = 8, 8

    # sides
    top, t = 9, 9
    bottom, b = 10, 10
    left, l = 11, 11
    right, r = 12, 12


class ScrollBar(pygame.sprite.Sprite):
    def __init__(self,
                 surface: pygame.Surface,
                 start_p: Callable[[int, int], tuple[int, int]],
                 end_p: Callable[[int, int], tuple[int, int]],
                 dim,
                 color_front,
                 color_back,
                 orientation='vertical',
                 start_pos=None,
                 alignment: AlignmentTypes = AlignmentTypes.tl) -> None:
        """
        Scroll bar is currently composed of a background rect and a slider which can be moved by scrolling

        :param surface: where the scroll bar will be drawn on
        :param start_p_func (): A function to calculate the starting position of the background rect (the minimum horizontal/vertical position of the
        scroll bar)
        :param end_p_func: Similar to start_p but the end position instead
        :param dim: Dimension of the slider
        :param color_front: Color of the slider
        :param color_back: Color of the background rect
        :param orientation: The axis the scroll bar moves when scrolling
        """
        super().__init__()
        self.surface, self.start_pos, self.end_pos, self.dim, self.orientation, self.alignment = \
            surface, start_p, end_p, dim, orientation, alignment
        self.back_color = color_back
        self.image = pygame.Surface(dim)
        self.image.fill(color_front)
        self.rect = self.image.get_rect()
        self.pos = start_pos if start_pos is not None else start_p
        self.back_rect = pygame.Rect(self.start_pos, [self.end_pos[0] - self.start_pos[0],
                                                      self.end_pos[1] - self.start_pos[1]])
        self.group = pygame.sprite.Group(self)
        self.step_size = None
        self.set_pos(self.pos)
    
    @property
    def percentage(self):
        if self.orientation == 'vertical':
            percentage = (self.back_rect.top - self.rect.top) / \
                         (self.back_rect.height - self.rect.height)
        else:
            percentage = (self.rect.left - self.back_rect.left ) / \
                         (self.back_rect.width - self.rect.width)
        return percentage

    def update(self, *args, move=None, screen_change=False, args_c=None) -> None | float | int:
        if move is not None:
            original = self.rect.topleft
            if self.orientation == 'vertical':
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] + move  # these are tuples
            else:
                self.rect.topleft = self.rect.topleft[0] + move, self.rect.topleft[1]
            self.check_slider_pos()
            index = 1 if self.orientation == 'vertical' else 0
            return abs(self.rect.topleft[index] - original[index])
        if screen_change:
            self.back_rect = pygame.Rect(self.start_pos, [self.end_pos[0] - self.start_pos[0],
                                                          self.end_pos[1] - self.start_pos[1]])
        pygame.draw.rect(self.surface, self.back_color, self.back_rect)
        self.group.draw(self.surface)
        for thing in args:
            text = pygame.font.Font('Assets/Fonts/Roboto-Light.ttf', 20).render(str(thing), True, args_c)
            self.surface.blit(text, text.get_rect(center=(self.rect.centerx, self.rect.centery)))

    def check_slider_pos(self):
        if self.orientation == 'vertical':
            if self.rect.bottomright[1] > self.end_pos[1]:
                self.rect.bottomright = self.rect.bottomright[0], self.end_pos[1]
            elif self.rect.topleft[1] < self.start_pos[1]:
                self.rect.topleft = self.rect.topleft[0], self.start_pos[1]
        else:
            if self.rect.bottomright[0] > self.end_pos[0]:
                self.rect.bottomright = self.end_pos[0], self.rect.bottomright[1]
            elif self.rect.topleft[0] < self.start_pos[0]:
                self.rect.topleft = self.start_pos[0], self.rect.topleft[1]

    def click_drag(self, clicked_pos) -> float | int | None:
        """
        :param clicked_pos: where the mouse clicked
        """
        index = 0 if self.orientation == 'horizontal' else 1
        if index == 0:
            self.rect.center = clicked_pos[0], self.rect.center[1]
        else:
            self.rect.center = self.rect.center[0], clicked_pos[1]
        self.check_slider_pos()
        if self.step_size:
            return (self.rect.topleft[index] - self.start_pos[index]) / self.step_size

    def set_percentage(self, percent):
        if self.orientation == 'vertical':
            self.set_pos((self.back_rect.top - self.rect.top) * percent + self.rect.top)
        else:
            self.set_pos((self.rect.left - self.back_rect.left ) * percent + self.back_rect.left, AlignmentTypes.r)
    
    def set_pos(self,
                pos: list | tuple | int | float,
                alignment: AlignmentTypes = None) -> None:
        """Setting self.pos to pos and setting a specific part of the sprite's rect based off its alignment"""
        if alignment: self.alignment = alignment
        if isinstance(pos, list | tuple):
            self.pos = tuple(pos)
        else:
            if self.alignment == AlignmentTypes.l or self.alignment == AlignmentTypes.r:
                self.pos = pos, self.pos[1]
            else:
                self.pos = self.pos[0], pos
        if self.alignment == AlignmentTypes.c:
            self.rect.center = self.pos

        # corners
        elif self.alignment == AlignmentTypes.tl:
            self.rect.topleft = self.pos
        elif self.alignment == AlignmentTypes.tr:
            self.rect.topright = self.pos
        elif self.alignment == AlignmentTypes.bl:
            self.rect.bottomleft = self.pos
        elif self.alignment == AlignmentTypes.br:
            self.rect.bottomright = self.pos

        # center of sides
        elif self.alignment == AlignmentTypes.mt:
            self.rect.midtop = self.pos
        elif self.alignment == AlignmentTypes.mb:
            self.rect.midbottom = self.pos
        elif self.alignment == AlignmentTypes.ml:
            self.rect.midleft = self.pos
        elif self.alignment == AlignmentTypes.mr:
            self.rect.midright = self.pos

        # sides
        elif self.alignment == AlignmentTypes.t:
            self.rect.top = self.pos[1]
        elif self.alignment == AlignmentTypes.b:
            self.rect.bottom = self.pos[1]
        elif self.alignment == AlignmentTypes.l:
            self.rect.left = self.pos[0]
        elif self.alignment == AlignmentTypes.r:
            self.rect.right = self.pos[0]


def draw_rect_alpha(surface, color, rect, width=4, border_radius=5):
    if pygame.Rect(rect).bottom > 0:
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), width=width, border_radius=border_radius)
        surface.blit(shape_surf, rect)


def make_text(screen, x, y, what, t_size=24, color='blue'):
    if y > -1:
        text = pygame.font.Font('Assets/Fonts/Roboto-Light.ttf', t_size).render(str(what), True, color)
        screen.blit(text, text.get_rect(center=(x, y)))
        return True
