"""
This file handels displaying the menu screen.

TODO: decrease load time
"""


import pygame
from .interfaces import *
from .UI import Button, ScrollBar
from .screen import Screen
from constants import *


class Menu(Screen):
    """
    This class handels displaying the menu and player interaction.
    """
    level_amount = 10
    dy = 0
    mouse_down = False
    slider_velocity = 0
    prev_time = pygame.time.get_ticks()

    levels_surface: pygame.surface.Surface
        
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs) -> None:
        """
        Creates a menu object.

        Args:
            screen (pygame.Surface): The surface that the level object will draw itself on.
            clock (pygame.time.Clock): The clock which will be used to set the maximum fps.
            **kwargs (Any): Any other arguments, will ignore all values other than `high_scores`.
                high_scores (dict[str, float]): The high scores of the player.
        
        Returns:
            None

        Raises:
            ValueError: If `high_scores` is not included in `kwargs`.
        """
        tmp = kwargs.copy()
        arguments = {'high_scores': dict}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        
        kwargs = tmp
        for arg, arg_type in arguments.items():
            if arg not in kwargs or not isinstance(kwargs[arg], arg_type):
                raise ValueError("Key word argument not included or is of an unacceptable type.")
        
        super().__init__(screen, clock, **kwargs)

        self.levels_surface = pygame.surface.Surface([self.screen.get_width() - 10, 60 * self.level_amount])
        self._high_scores_init()
        self._stars_init()
        self._misc_init()
        
        self._level_init()
        self._slider_init()

        self._render_levels_surface()
    
    def _render_levels_surface(self) -> None:
        """
        Renders the level surface which will be moved by the slider.
        
        Returns:
            None
        """
        self.levels_surface = pygame.surface.Surface([self.screen.get_width() - 10, 60 * self.level_amount])
        self.levels_surface.fill(BACKGROUND_COLOR)
        to_draw = pygame.sprite.Group()
        for sprite in self.level_select_g.sprites() + self.high_score_g.sprites() + self.stars_g.sprites() + self.lock_g.sprites():
            sprite: Button
            sprite.change_surface(self.levels_surface)
            to_draw.add(sprite)
        
        for i, sprite in enumerate(self.level_select_l):
            sprite.set_pos((74, i * 60))
        for i, sprite in enumerate(self.high_score_l):
            sprite.set_pos((self.levels_surface.get_width() - 100, i * 60))
        for i, sprite in enumerate(self.stars_l):
            sprite.set_pos((self.levels_surface.get_width() - 40, i * 60))
        for i, sprite in enumerate(self.lock_l):
            sprite.set_pos((5, INV_REQUIREMENTS[int(sprite.text)] * 60))
        
        to_draw.draw(self.levels_surface)
        to_draw.update()
    
    def loop(self) -> Redirect:
        """
        The main game loop.

        Returns:
            Redirect: A screen redirect.
        
        Raises:
            ExitException: If the user exits out of the screen.
        """
        while True:
            dt = (pygame.time.get_ticks() - self.prev_time) / 1000
            dt *= 60
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                elif event.type == pygame.VIDEORESIZE:
                    self._video_resize()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Redirect(ScreenID.intro)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        res_val = self._left_click()
                        if res_val is not None:
                            return res_val
                    elif event.button == 4:
                        self.slider_velocity -= dt * 4
                    elif event.button == 5:
                        self.slider_velocity += dt * 4
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False
            self.prev_time = pygame.time.get_ticks()
            
            self._slider_update()
            self._draw()

    def _level_init(self) -> None:
        """
        Initializes the level buttons.

        Returns:
            None
        """
        self.level_select_g = pygame.sprite.Group()
        self.level_select_l = []

        self.lock_g = pygame.sprite.Group()
        self.lock_l = []
        for _i in range(self.level_amount):
            try:  # if song is written
                locked = REQUIREMENTS[_i] > self.star_count
                directory = SONG_PATHS[_i]
                if locked:
                    self.lock_l.append(Button(self.levels_surface, [0, _i * 60], None, REQUIREMENTS[_i], 30, alignment_pos='topleft',
                                        path='Assets/Images/lock.png', dim=(59, 59)))
            except KeyError:  # if song doesn't exist
                locked = True
                directory = "/To be discovered."
                self.lock_l.append(Button(self.levels_surface, [0, _i * 60], None, REQUIREMENTS[_i], 30, alignment_pos='topleft',
                                        path='Assets/Images/lock.png', dim=(59, 59)))
            name = directory[directory.find("/") + 1:directory.find(".")]
            self.level_select_l.append(
                Button(self.levels_surface, [90, _i * 60], None if locked else _i, "To be discovered" if locked else name, 30, alignment_pos='topleft'))
        self.total_items_len = self.level_select_l[-1].rect.bottom - self.level_select_l[0].rect.top - self.screen.get_height() + 100
        self.lock_g.add(self.lock_l)
        self.level_select_g.add(self.level_select_l)

    def _slider_init(self) -> None:
        """
        Initializes the slider.

        Returns:
            None
        """
        self.slider = ScrollBar(self.screen, [0, 100], [10, self.screen.get_height()], [10, 50], 'black', 'dark gray')
        self.slider_g = pygame.sprite.GroupSingle(self.slider)
        self.index = 1 if self.slider.orientation == 'vertical' else 0
        self.slider.step_size = (self.slider.end_pos[self.index] - self.slider.start_pos[self.index] - self.slider.dim[self.index]) / self.total_items_len

    def _misc_init(self) -> None:
        """
        Initializes other buttons.

        Returns:
            None
        """
        self.misc_g = pygame.sprite.Group()
        self.misc_l = [
            Button(self.screen, [self.screen.get_width() / 2, 50], None, 'Choose a Level!', 50),
            Button(self.screen, [self.screen.get_width(), 10], None, self.star_count, 50, alignment_pos='topright')
        ]
        self.misc_g.add(self.misc_l)

    def _stars_init(self) -> None:
        """
        Initializes the star buttons.

        Returns:
            None
        """
        self.stars_g = pygame.sprite.Group()
        self.stars_l = []
        self.star_count = 0
        for _i in range(self.level_amount):
            star_count = self._calc_stars(_i)
            self.star_count += star_count
            self.stars_l.append(
                Button(self.levels_surface, [self.levels_surface.get_width() - 40, _i * 60], None, star_count, 30, path='Assets/Images/star.png',
                    dim=(59, 59), alignment_pos='topright')
            )
        self.stars_g.add(self.stars_l)

    def _high_scores_init(self) -> None:
        """
        Initializes the buttons displaying high scores.
        
        Returns:
            None
        """
        self.high_score_g = pygame.sprite.Group()
        self.high_score_l = []
        for _i in range(self.level_amount):
            score = self._get_score(_i)
            self.high_score_l.append(
                Button(self.levels_surface, [self.levels_surface.get_width() - 100, _i * 60], _i, round(float(score), 2), 30, alignment_pos='topright')
            )
        self.high_score_g.add(self.high_score_l)
    
    def _left_click(self) -> Redirect | None:
        """
        Updates buttons based on left click.

        Returns:
            Redirect: If the user clicks on certain buttons.
            None: If the user clicks on other buttons.
        """
        clicked_pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.level_select_g.sprites()):
            if sprite.rect.collidepoint(clicked_pos) and isinstance(self.level_select_l[i].mode_c, int):
                self.song_id = self.level_select_l[i].mode_c
                return Redirect(ScreenID.levelOptions, song_id=self.song_id)
        if self.slider.back_rect.collidepoint(clicked_pos):
            self.mouse_down = True
            self.dy = self.slider.click_drag(clicked_pos)

    def _video_resize(self) -> None:
        """
        Updates the slider based on a screen resize event.

        Returns:
            None
        """
        self._render_levels_surface()
        self.slider.end_pos = [10, self.screen.get_height()]
        self.slider.update(screen_change=True)
        self.total_items_len = self.level_select_l[-1].rect.bottom - self.level_select_l[0].rect.top - self.screen.get_height() + 100
        self.index = 1 if self.slider.orientation == 'vertical' else 0
        self.slider.step_size = (self.slider.end_pos[self.index] - self.slider.start_pos[self.index] - self.slider.dim[self.index]) / self.total_items_len
        self.slider.step_size = self.slider.step_size
        self.misc_l[0].rect.center = [self.screen.get_width() / 2, 50]

    def _draw(self) -> None:
        """
        Draws all elements onto the screen.

        Returns:
            None
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.levels_surface, [10, 95 - self.dy])
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (0, 0, self.screen.get_width(), 95))
        self.misc_g.draw(self.screen)
        self.misc_g.update()
        if self.total_items_len > 0:
            self.slider_g.update()
            self.slider_g.draw(self.screen)
        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def _slider_update(self) -> None:
        """
        Updates the slider.

        Returns:
            None
        """
        if self.mouse_down:
            self.dy = self.slider.click_drag(pygame.mouse.get_pos())
        if self.total_items_len > 0:
            self.slider_velocity *= .9
            if abs(self.slider_velocity) < 1:
                self.slider_velocity = 0
            self.dy += self.slider_velocity
            if self.dy < 0:
                self.dy = 0
                self.slider_velocity = 0
            elif self.dy > self.total_items_len:
                self.dy = self.total_items_len
                self.slider_velocity = 0
            self.slider.rect.topleft = self.slider.rect.topleft[0], self.dy * self.slider.step_size + self.slider.start_pos[1]
        else:
            self.dy = 0

    def _get_score(self, i) -> float:
        """
        Gets the high scores of level `i`.

        Args:
            i (int): The level id.
        
        Returns:
            Score (float): The score.
        """
        if str(i) not in self.high_scores:
            score = 0
        else:
            score = self.high_scores[str(i)]
        if str(i) + 'e' in self.high_scores:
            score += self.high_scores[str(i) + 'e']
        return score

    def _calc_stars(self, i) -> int:
        """
        Calculates the number of stars.

        Returns:
            Stars (int): The number of stars based on high scores.
        """
        high_score = self._get_score(i)
        for score, stars in SCORE2STARS.items():
            if high_score <= score:
                return stars
        