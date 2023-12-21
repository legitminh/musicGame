import pygame
from interfaces import *
from UI import Button, Screen, ScrollBar
from constants import *


class Menu(Screen):
    def loop(self):
        """
        params: screen, clock
        **kwargs: high_scores        
        """
        # high score
        level_amount = 10
        up = 0
        high_score_g = pygame.sprite.Group()
        high_score_l = []
        for _i in range(level_amount):
            try:
                name = self.high_scores[str(_i)]
            except KeyError:
                name = 0
            high_score_l.append(
                Button(self.screen, [self.screen.get_width() - 100, _i * 60 + 95 - up], _i, round(float(name), 2), 30, alignment_pos='topright')
            )
        high_score_g.add(high_score_l)
        # star
        stars_g = pygame.sprite.Group()
        stars_l = []
        stars = 0
        for _i in range(level_amount):
            try:
                if 0 <= self.high_scores[str(_i)] < 50:
                    star = 0
                elif self.high_scores[str(_i)] < 75:
                    star = 1
                elif self.high_scores[str(_i)] < 90:
                    star = 2
                elif self.high_scores[str(_i)] < 100:
                    star = 3
                else:
                    star = 5
            except KeyError:
                star = 0
            try:
                _i = str(_i) + 'e'
                if 0 <= self.high_scores[str(_i)] < 50:
                    star += 0
                elif self.high_scores[str(_i)] < 75:
                    star += 1
                elif self.high_scores[str(_i)] < 90:
                    star += 2
                elif self.high_scores[str(_i)] < 100:
                    star += 3
                else:
                    star += 5
            except KeyError:
                star += 0
            stars += star
            _i = int(_i.replace('e', ''))
            stars_l.append(
                Button(self.screen, [self.screen.get_width(), _i * 60 + 95 - up], None, star, 30, path='Assets/star.png',
                    dim=(59, 59), alignment_pos='topright')
            )
        stars_g.add(stars_l)
        # self.screen title and stars N
        others_g = pygame.sprite.Group()
        others_l = [
            Button(self.screen, [self.screen.get_width() / 2, 50], None, 'Choose a Level!', 50),
            Button(self.screen, [self.screen.get_width(), 10], None, stars, 50, alignment_pos='topright')
        ]
        others_g.add(others_l)
        # songs and locks display
        level_select_g = pygame.sprite.Group()
        level_select_l = []
        lock_g = pygame.sprite.Group()
        lock_l = []
        for _i in range(level_amount):
            try:  # if song is written
                locked = REQUIREMENTS[_i] > stars
                directory = SONGS[_i]
                if locked:
                    lock_l.append(Button(self.screen, [10, _i * 60 + 95 - up], None, REQUIREMENTS[_i], 30, alignment_pos='topleft',
                                        path='Assets/lock.png', dim=(59, 59)))
            except KeyError:  # if song doesn't exist
                locked = True
                directory = "/To be discovered."
            name = directory[directory.find("/") + 1:directory.find(".")]
            level_select_l.append(
                Button(self.screen, [100, _i * 60 + 95 - up], "To be discovered" if locked else _i, name, 30, alignment_pos='topleft'))
        lock_g.add(lock_l)
        level_select_g.add(level_select_l)
        # slider
        slider = ScrollBar(self.screen, [0, 100], [10, self.screen.get_height()], [10, 50], 'black', 'dark gray')
        slider_g = pygame.sprite.GroupSingle(slider)
        velocity = 0
        last_time = pygame.time.get_ticks()
        total_len = level_select_l[-1].rect.bottom - level_select_l[0].rect.top - self.screen.get_height() + 100
        index = 1 if slider.orientation == 'vertical' else 0
        slider_step_size = (slider.end_pos[index] - slider.start_pos[index] - slider.dim[index]) / total_len
        slider.step_size = slider_step_size
        level_select_g.add(level_select_l)
        mouse_down = False
        while True:
            dt = (pygame.time.get_ticks() - last_time) / 1000
            dt *= 60
            last_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                elif event.type == pygame.VIDEORESIZE:
                    slider.end_pos = [10, self.screen.get_height()]
                    slider.update(screen_change=True)
                    total_len = level_select_l[-1].rect.bottom - level_select_l[0].rect.top - self.screen.get_height() + 100
                    index = 1 if slider.orientation == 'vertical' else 0
                    slider_step_size = (slider.end_pos[index] - slider.start_pos[index] - slider.dim[index]) / total_len
                    slider.step_size = slider_step_size
                    others_l[0].rect.center = [self.screen.get_width() / 2, 50]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return ScreenID.intro
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_pos = pygame.mouse.get_pos()
                        for i in range(len(level_select_g.sprites())):
                            s = level_select_g.sprites()[i]
                            if s.rect.collidepoint(clicked_pos) and isinstance(level_select_l[i].mode_c, int):
                                self.song_id = str(level_select_l[i].mode_c)
                                return ScreenID.levelOptions
                        if slider.back_rect.collidepoint(clicked_pos):
                            mouse_down = True
                            up = slider.click_drag(clicked_pos)
                    elif event.button == 4:
                        velocity -= dt * 4
                    elif event.button == 5:
                        velocity += dt * 4
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
            if mouse_down:
                up = slider.click_drag(pygame.mouse.get_pos())
            if total_len > 0:
                velocity *= .9
                if abs(velocity) < 1:
                    velocity = 0
                up += velocity
                if up < 0:
                    up = 0
                    velocity = 0
                elif up > total_len:
                    up = total_len
                    velocity = 0
                slider.rect.topleft = slider.rect.topleft[0], up * slider_step_size + slider.start_pos[1]
            else:
                up = 0
            for i, sprite in enumerate(level_select_l):
                sprite.set_pos((84, i * 60 + 95 - up))
            width = self.screen.get_width()
            for i, sprite in enumerate(high_score_l):
                sprite.set_pos((width - 100, i * 60 + 95 - up))
            for i, sprite in enumerate(stars_l):
                sprite.set_pos((width - 40, i * 60 + 93 - up))
            for i, sprite in enumerate(lock_l):
                sprite.set_pos((15, INVREQUIREMENTS[int(sprite.text)] * 60 + 95 - up))
            self.screen.fill('light gray')
            height = self.screen.get_height()
            to_draw = pygame.sprite.Group()
            for sprite in level_select_g.sprites() + high_score_g.sprites() + stars_g.sprites() + lock_g.sprites():
                if height > sprite.rect.top and sprite.rect.bottom > 95:
                    to_draw.add(sprite)
            to_draw.draw(self.screen)
            to_draw.update()
            pygame.draw.rect(self.screen, 'light gray', (0, 0, width, 95))
            others_g.draw(self.screen)
            others_g.update()
            if total_len > 0:
                slider_g.update()
                slider_g.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FRAME_RATE)
