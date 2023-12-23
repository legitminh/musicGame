import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *


class Intro(Screen):
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs):
        super().__init__(screen, clock, **kwargs)
        self.intro_g = pygame.sprite.Group()
        self.intro_l = [
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 - 50], None, 'Typing Piano', 50),
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 50], ScreenID.menu, 'Play', 30),
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 100], ScreenID.option, 'Options', 30)
        ]
        self.intro_g.add(self.intro_l)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise ExitException()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ret_val = self._button_clicked()
                    if ret_val is not None:
                        return ret_val
            self._draw()

    def _draw(self):
        self.screen.fill('light gray')
        self.clock.tick(FRAME_RATE)
        self.intro_g.draw(self.screen)
        self.intro_g.update()
        pygame.display.update()

    def _button_clicked(self):
        x, y = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.intro_g.sprites()):
            if sprite.rect.collidepoint(x, y):
                return self.intro_l[i].mode_c
        return None
