import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *


class Intro(Screen):
    def loop(self):
        """
        :params: screen, clock
        **kwargs: None
        """
        intro_g = pygame.sprite.Group()
        intro_l = [
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 - 50], None, 'Typing Piano', 50),
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 50], ScreenID.menu, 'Play', 30),
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 100], ScreenID.option, 'Options', 30)
        ]
        intro_g.add(intro_l)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        raise ExitException()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(len(intro_g.sprites())):
                            s = intro_g.sprites()[i]
                            pos = pygame.mouse.get_pos()
                            if s.rect.collidepoint(pos[0], pos[1]) and intro_l[i].mode_c is not None:
                                return intro_l[i].mode_c
            self.screen.fill('light gray')
            self.clock.tick(FRAME_RATE)
            intro_g.draw(self.screen)
            intro_g.update()
            pygame.display.update()
