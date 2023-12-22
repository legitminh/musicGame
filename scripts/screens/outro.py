import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *

class Outro(Screen):
    def loop(self):
        """
        :params: screen, clock
        **kwargs: song_id, score, slowdown, high_scores
        """
        self.update_high_scores()
        outro_g = pygame.sprite.Group()
        if isinstance(self.song_id, str):
            directory = SONGS[int(self.song_id.replace('e', '').replace('p', ''))]
        else:
            directory = SONGS[self.song_id]
        
        outro_l = [Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 + 50], self.song_id, 'Play again', 30),
                Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 - 50], '',
                        f'You scored {self.score:.2f}% on {directory[directory.find("/") + 1:directory.find(".")]}',
                        30),
                Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 + 110], ScreenID.menu,
                        'Return to level selection', 30)]
        outro_g.add(outro_l)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return ScreenID.menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(len(outro_g.sprites())):
                            s = outro_g.sprites()[i]
                            pos = pygame.mouse.get_pos()
                            if s.rect.collidepoint(pos[0], pos[1]) and (
                                    isinstance(outro_l[i].mode_c, int) or outro_l[i].mode_c):
                                if isinstance(outro_l[i].mode_c, str):  # extreme
                                    self.song_id = outro_l[i].mode_c
                                    return ScreenID.level
                                if isinstance(outro_l[i].mode_c, int):
                                    self.song_id = outro_l[i].mode_c
                                    return ScreenID.level
                                return outro_l[i].mode_c
            self.screen.fill('light gray')
            outro_g.draw(self.screen)
            outro_g.update()
            pygame.display.update()

    def update_high_scores(self):
        if self.slowdown < 1:
            return 
        if str(self.song_id) not in self.high_scores:
            self.high_scores[str(self.song_id)] = self.score
            return
        if self.score > self.high_scores[str(self.song_id)]:
            self.high_scores[str(self.song_id)] = self.score
