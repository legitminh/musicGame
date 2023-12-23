import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *

class LevelOptions(Screen):
    high_scores: dict[str, float]

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs):
        super().__init__(screen, clock, **kwargs)
        self.song_id = str(self.song_id).replace('e', '')
        self.slowdown = 1
        self._mode_buttons_init()
        self._lock_init()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                elif event.type == pygame.VIDEORESIZE:
                    self._video_resize()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Redirect(ScreenID.menu)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ret_val = self._button_clicked()
                    if ret_val is not None:
                        return ret_val
            self._draw()

    def _lock_init(self):
        self.lock_g = pygame.sprite.GroupSingle()
        if self.song_id not in self.high_scores or self.high_scores[self.song_id] != 100:
            self.lock_g.add(Button(self.screen, self.modes_l[5].rect.center, '', 0, 0, path='Assets/lock.png',
                            dim=(50, 50), alignment_pos='center'))

    def _mode_buttons_init(self):
        self.modes_l = [
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2 - 130], None, 'Speed', 30),
            Button(self.screen, [self.screen.get_width() / 2 - 105, self.screen.get_height() / 2 - 65], '.75', '75%', 30),
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2 - 65], '.50', '50%', 30),
            Button(self.screen, [self.screen.get_width() / 2 + 105, self.screen.get_height() / 2 - 65], '.25', '25%', 30),
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2], int(self.song_id), 'Normal', 30),
            Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() / 2 + 65], self.song_id + 'e', 'Extreme', 30)
        ]
        self.modes_g = pygame.sprite.Group()
        self.modes_g.add(self.modes_l)
    
    def _draw(self):
        self.screen.fill('light gray')
        self.modes_g.draw(self.screen)
        self.modes_g.update()
        if self.song_id not in self.high_scores or self.high_scores[self.song_id] != 100:
            self.lock_g.draw(self.screen)
            self.lock_g.update()
        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def _button_clicked(self):
        clicked_pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.modes_g.sprites()):
            if not sprite.rect.collidepoint(clicked_pos):
                continue
            if self.modes_l[i].mode_c is None:
                continue
            if '.' in str(self.modes_l[i].mode_c):
                self._change_slowdown(i)
                break
            if self.modes_l[i].mode_c in SONGS:
                return Redirect(ScreenID.level, slowdown=self.slowdown, song_id=self.song_id)
            if self.song_id in self.high_scores:
                return Redirect(ScreenID.level, slowdown=self.slowdown, song_id=self.song_id + 'e')
            break

    def _change_slowdown(self, sprite_i):
        if float(self.modes_l[sprite_i].mode_c) == self.slowdown:
            self.slowdown = 1
            self.modes_l[sprite_i].color_changer((150, 150, 150, 255))
        else:
            for sprite in self.modes_l[1:4]:
                sprite.color_changer((150, 150, 150, 255))
            self.slowdown = float(self.modes_l[sprite_i].mode_c)
            self.modes_l[sprite_i].color_changer((0, 150, 0, 255))

    def _video_resize(self):
        for i, button in enumerate(self.modes_l):
                        # button.rect.center = self.screen.get_width() / 2, self.screen.get_height() / 2 + 65
            self.screen.get_width() / 2, self.screen.get_height() / 2 + 50 * (i - 1) - (0 if i else 65)
