import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *

class LevelOptions(Screen):
    def loop(self):
        """
        :param: screen, clock
        **kwargs: highscore, song_id
        """
        self.song_id = str(self.song_id)
        # modes
        modes_l = [
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2 - 130], None, 'Speed', 30),
            Button(self.screen, [self.screen.get_width() / 2 - 105, self.screen.get_height() / 2 - 65], '.75', '75%', 30),
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2 - 65], '.50', '50%', 30),
            Button(self.screen, [self.screen.get_width() / 2 + 105, self.screen.get_height() / 2 - 65], '.25', '25%', 30),
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2], int(self.song_id), 'Normal', 30),
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2 + 65], self.song_id + 'e', 'Extreme', 30)
        ]
        modes_g = pygame.sprite.Group()
        modes_g.add(modes_l)
        # lock
        lock_g = pygame.sprite.GroupSingle()
        if self.song_id not in self.high_scores or self.high_scores[self.song_id] != 100:
            lock_g.add(Button(self.screen, modes_l[5].rect.center, '', 0, 0, path='Assets/lock.png',
                            dim=(50, 50), alignment_pos='center'))
        slowdown = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    for i, button in enumerate(modes_l):
                        # button.rect.center = self.screen.get_width() / 2, self.screen.get_height() / 2 + 65
                        self.screen.get_width() / 2, self.screen.get_height() / 2 + 50 * (i - 1) - (0 if i else 65)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return ScreenID.menu
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_pos = pygame.mouse.get_pos()
                        for i in range(len(modes_g.sprites())):
                            if modes_g.sprites()[i].rect.collidepoint(clicked_pos):
                                if '.' in str(modes_l[i].mode_c):
                                    if float(modes_l[i].mode_c) == slowdown:
                                        slowdown = 1
                                        modes_l[i].color_changer((150, 150, 150, 255))
                                    else:
                                        for sprite in modes_l[1:4]:
                                            sprite.color_changer((150, 150, 150, 255))
                                        slowdown = float(modes_l[i].mode_c)
                                        modes_l[i].color_changer((0, 150, 0, 255))
                                    break
                                if 'e' in str(modes_l[i].mode_c) and self.high_scores[self.song_id] == 100:
                                    self.slowdown = slowdown
                                    self.song_id = modes_l[i].mode_c
                                    return ScreenID.level
                                elif 'e' not in str(modes_l[i].mode_c) and (modes_l[i].mode_c or modes_l[i].mode_c == 0):
                                    self.slowdown = slowdown
                                    self.song_id = modes_l[i].mode_c
                                    return ScreenID.level
            self.screen.fill('light gray')
            modes_g.draw(self.screen)
            modes_g.update()
            if self.song_id not in self.high_scores or self.high_scores[self.song_id] != 100:
                lock_g.draw(self.screen)
                lock_g.update()
            pygame.display.update()
            self.clock.tick(FRAME_RATE)
