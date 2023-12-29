"""
This file handels displaying the level options screen.
"""
import pygame
from interfaces import *
from UI import Button
from .screen import Screen
from constants import *

class LevelOptions(Screen):
    """
    This class handels displaying the level options screen and player interactions.
    """
    high_scores: dict[str, float]

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs) -> None:
        """
        Creates a Level options object.

        Args:
            screen (pygame.Surface): The surface that the level object will draw itself on.
            clock (pygame.time.Clock): The clock which will be used to set the maximum fps.
            **kwargs (Any): Any other arguments, will ignore all values other than `song_id`.
                song_id (int): The id of the song that will be played.
        
        Returns:
            None

        Raises:
            ValueError: If `song_id` is not included in `kwargs`.
        """
        tmp = kwargs.copy()
        arguments = {'song_id': int}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        
        kwargs = tmp
        for arg, arg_type in arguments.items():
            if arg not in kwargs or not isinstance(kwargs[arg], arg_type):
                raise ValueError("Key word argument not included or is of an unacceptable type.")
        
        super().__init__(screen, clock, **kwargs)
        self.song_id = str(self.song_id).replace('e', '')
        self.slowdown = 1
        self._mode_buttons_init()
        self._lock_init()

    def loop(self) -> Redirect:
        """
        The main game loop.

        Returns:
            Redirect: A screen redirect.
        
        Raises:
            ExitException: If the user exits out of the screen.
        """
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

    def _lock_init(self) -> None:
        """
        Initializes the locks.

        Returns:
            None
        """
        self.lock_g = pygame.sprite.GroupSingle()
        if self.song_id not in self.high_scores or self.high_scores[self.song_id] != 100:
            self.lock_g.add(Button(self.screen, self.modes_l[5].rect.center, '', 0, 0, path='Assets/Images/lock.png',
                            dim=(50, 50), alignment_pos='center'))

    def _mode_buttons_init(self) -> None:
        """
        Initializes buttons.

        Returns:
            None
        """
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
    
    def _draw(self) -> None:
        """
        Draws all elements onto the screen.

        Returns:
            None
        """
        self.screen.fill('light gray')
        self.modes_g.draw(self.screen)
        self.modes_g.update()
        if self.song_id not in self.high_scores or self.high_scores[self.song_id] != 100:
            self.lock_g.draw(self.screen)
            self.lock_g.update()
        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def _button_clicked(self) -> Redirect | None:
        """
        Updates the buttons on click.

        Returns:
            Redirect: If the click event was on certain buttons.
            None: If the click event was on other buttons.
        """
        clicked_pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.modes_g.sprites()):
            if not sprite.rect.collidepoint(clicked_pos):
                continue
            if self.modes_l[i].mode_c is None:
                continue
            if '.' in str(self.modes_l[i].mode_c):
                self._change_slowdown(i)
                break
            if self.modes_l[i].mode_c in SONG_PATHS:
                return Redirect(ScreenID.level, slowdown=self.slowdown, song_id=self.song_id, extreme=False)
            if self.song_id in self.high_scores:
                return Redirect(ScreenID.level, slowdown=self.slowdown, song_id=self.song_id, extreme=True)
            break

    def _change_slowdown(self, sprite_i) -> None:
        """
        Changes the slow down if the click was on a "slow down" button.

        Returns:
            None
        """
        if float(self.modes_l[sprite_i].mode_c) == self.slowdown:
            self.slowdown = 1
            self.modes_l[sprite_i].color_changer((150, 150, 150, 255))
        else:
            for sprite in self.modes_l[1:4]:
                sprite.color_changer((150, 150, 150, 255))
            self.slowdown = float(self.modes_l[sprite_i].mode_c)
            self.modes_l[sprite_i].color_changer((0, 150, 0, 255))

    def _video_resize(self) -> None:
        """
        Updates the slider on the screen resize.

        Returns:
            None
        """
        for i, button in enumerate(self.modes_l):
                        # button.rect.center = self.screen.get_width() / 2, self.screen.get_height() / 2 + 65
            self.screen.get_width() / 2, self.screen.get_height() / 2 + 50 * (i - 1) - (0 if i else 65)
