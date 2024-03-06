"""
This files handels displaying the intro screen.
"""


import pygame
from .interfaces import *
from .UI import Button
from .screen import Screen
from constants import *


class Intro(Screen):
    """
    This class handels displaying the intro and player interaction.
    """
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs) -> None:
        """
        Creates a intro object.

        Args:
            screen (pygame.Surface): The surface that the level object will draw itself on.
            clock (pygame.time.Clock): The clock which will be used to set the maximum fps.
            **kwargs (Any): Any other arguments, will ignore all values.

        Returns:
            None
        """
        tmp = kwargs.copy()
        arguments = {'volume': float, 'song_id': int, 'extreme': bool, 'slowdown': float}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        kwargs = tmp

        super().__init__(screen, clock, **kwargs)
        self.intro_g = pygame.sprite.Group()
        self.intro_l = [
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 - 50], None, 'Typing Piano', 50),
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 50], ScreenID.menu, 'Play', 30),
            Button(self.screen, [self.screen.get_width() // 2, self.screen.get_height() // 2 + 100], ScreenID.option, 'Options', 30)
        ]
        self.intro_g.add(self.intro_l)
        self._draw()

    def loop(self) -> Redirect | None:
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise ExitException()
                if event.type == pygame.VIDEORESIZE:
                    self._video_resize()
                    self._draw()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ret_val = self._button_clicked()
                    if ret_val is not None:
                        return ret_val
            self.clock.tick(FRAME_RATE)

    def _video_resize(self) -> None:
        """
        Updates all elements on the screen.
        
        Returns:
            None
        """
        for i, element in enumerate(self.intro_l):
            element.set_pos([self.screen.get_width() // 2, self.screen.get_height() // 2 + (-50, 50, 100)[i]])
        
        self._draw()

    def _draw(self) -> None:
        """
        Draws all elements onto the screen.
        This method is only called on init and when screen size changes.

        Returns:
            None
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.intro_g.draw(self.screen)
        self.intro_g.update()
        pygame.display.update()

    def _button_clicked(self) -> Redirect | None:
        """
        Updates the buttons based on click location and redirects if certain buttons are clicked.

        Returns:
            Redirect: If certain buttons are clicked.
            None: If other buttons are clicked.
        """
        x, y = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.intro_g.sprites()):
            if sprite.rect.collidepoint(x, y):
                redirect = Redirect(self.intro_l[i].mode_c)
                if redirect.redirect_screen is not None:
                    return redirect
        return None
