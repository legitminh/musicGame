import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *

class Outro(Screen):
    high_scores: dict[str, float]
    slowdown: float
    score: float

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs):
        super().__init__(screen, clock, **kwargs)
        self._buttons_init()

    def loop(self):
        self._update_high_scores()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Redirect(ScreenID.menu, high_score=self.high_scores)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ret_val = self._button_clicked()
                    if ret_val is not None:
                        return ret_val
            self._draw()

    def _buttons_init(self):
        self.outro_g = pygame.sprite.Group()
        if isinstance(self.song_id, str):
            directory = SONGS[int(self.song_id.replace('e', '').replace('p', ''))]
        else:
            directory = SONGS[self.song_id]
        
        self.outro_l = [Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 + 50], self.song_id, 'Play again', 30),
                Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 - 50], '',
                        f'You scored {self.score:.2f}% on {directory[directory.find("/") + 1:directory.find(".")]}',
                        30),
                Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 + 110], ScreenID.menu,
                        'Return to level selection', 30)]
        self.outro_g.add(self.outro_l)

    def _draw(self):
        self.screen.fill('light gray')
        self.outro_g.draw(self.screen)
        self.outro_g.update()
        pygame.display.update()

    def _button_clicked(self):
        pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.outro_g.sprites()):
            if not sprite.rect.collidepoint(*pos):
                continue
            if not (isinstance(self.outro_l[i].mode_c, int) or self.outro_l[i].mode_c):
                break
            if isinstance(self.outro_l[i].mode_c, str | int):
                return Redirect(ScreenID.level, song_id=self.outro_l[i].mode_c)
            return Redirect(self.outro_l[i].mode_c)

    def _update_high_scores(self):
        if self.slowdown < 1:
            return 
        if str(self.song_id) not in self.high_scores:
            self.high_scores[str(self.song_id)] = self.score
            return
        if self.score > self.high_scores[str(self.song_id)]:
            self.high_scores[str(self.song_id)] = self.score
