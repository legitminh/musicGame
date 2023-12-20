import pygame
from interfaces import *
from ..UI import Button, Screen


class Intro(Screen):
    def loop(self) -> mode_type:
        while True:
            intro_g = pygame.sprite.Group()
            intro_l = [
                Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 - 50], None, 'Typing Piano', 50),
                Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 50], Screens.menu, 'Play', 30),
                Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 100], Screens.option, 'Options', 30)
            ]
            intro_g.add(intro_l)
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
                                return (intro_l[i].mode_c, [])
            self.screen.fill('light gray')
            intro_g.draw(self.screen)
            intro_g.update()
            pygame.display.update()
