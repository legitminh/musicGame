"""
This file handels displaying the options screen.

TODO: player controls note speed (velocity)
"""


import pygame
from .interfaces import *
from .UI import Button, ScrollBar
from .screen import Screen
from constants import *

class Options(Screen):
    """
    This class handels displaying the options screen and player interaction.    
    """
    s_mouse_down = False
    v_mouse_down = False

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs) -> None:
        """
        Initializes the options screen.

        Args:
            screen (pygame.Surface): The surface that the level object will draw itself on.
            clock (pygame.time.Clock): The clock which will be used to set the maximum fps.
            **kwargs (Any): Any other arguments, will ignore all values other than `volume` and `velocity`.
                volume (float): The volume diplayed on the scroll bar.
                velocity (float): The velocity diplayed on the scroll bar.
        
        Returns:
            None
        
        Raises:
            ValueError: If `volume` is not included `kwargs`.
        """
        tmp = kwargs.copy()
        arguments = {'volume': float, 'velocity': float}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        
        kwargs = tmp
        for arg, arg_type in arguments.items():
            if arg not in kwargs or not isinstance(kwargs[arg], arg_type):
                raise ValueError("Key word argument not included or is of an unacceptable type.")

        super().__init__(screen, clock, **kwargs)
        self.user_interfaces = [
            Button(self.screen, [self.screen.get_width() / 2, 50], None, 'Options', 50),
            Button(self.screen, [self.screen.get_width() / 2, 125], None, 'Volume', 30),
            Button(self.screen, [self.screen.get_width() / 2, 225], None, 'Velocity', 30)
        ]
        self.others = pygame.sprite.Group(self.user_interfaces)
        self.sound_slider = ScrollBar(self.screen, [25, 160], [self.screen.get_width() - 25, 180], [50, 20], 'black', 'dark gray',
                                orientation='horizontal', start_pos=[25 + (self.volume * (self.screen.get_width() - 50 - 50)), 160])
        self.velocity_slider = ScrollBar(self.screen, [25, 260], [self.screen.get_width() - 25, 280], [50, 20], 'black', 'dark gray',
                                orientation='horizontal', start_pos=[25 + (self.velocity * (self.screen.get_width() - 50 - 50)), 260])
        self.sliders = pygame.sprite.Group()
        self.sliders.add(self.sound_slider)
        self.sliders.add(self.velocity_slider)

    def loop(self) -> None:
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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Redirect(ScreenID.intro, volume=self.volume, velocity=self.velocity)
                elif event.type == pygame.VIDEORESIZE:
                    self._video_resize()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._left_click()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.s_mouse_down = False
                    self.v_mouse_down = False
            if self.s_mouse_down:
                self.sound_slider.click_drag(pygame.mouse.get_pos())
            if self.v_mouse_down:
                self.velocity_slider.click_drag(pygame.mouse.get_pos())
            self._draw()

    def _draw(self) -> None:
        """
        Draws all elements onto the screen.

        Returns:
            None
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.volume = self.sound_slider.percentage
        self.velocity = self.velocity_slider.percentage
        self.sound_slider.update(f'{int(self.volume * 100)}%', args_c='white')
        self.velocity_slider.update(f'{100 + int(self.velocity * 1400)}', args_c='white')
        self.others.draw(self.screen)
        self.others.update()
        self.clock.tick(FRAME_RATE)
        pygame.display.update()

    def _video_resize(self) -> None:
        """
        Updates sliders on screen resize.

        Returns:
            None
        """
        self.sound_slider.end_pos = self.screen.get_width() - 25, 180
        self.sound_slider.update(screen_change=True)
        leng = self.sound_slider.end_pos[0] - self.sound_slider.start_pos[0] - self.sound_slider.rect.width
        self.sound_slider.rect.topleft = self.sound_slider.start_pos[0] + (self.volume * leng), 160

        self.velocity_slider.end_pos = self.screen.get_width() - 25, 280
        self.velocity_slider.update(screen_change=True)
        leng = self.velocity_slider.end_pos[0] - self.velocity_slider.start_pos[0] - self.velocity_slider.rect.width
        self.velocity_slider.rect.topleft = self.velocity_slider.start_pos[0] + (self.volume * leng), 260
        for sprite in self.user_interfaces:
            L = list(sprite.rect.center)
            L[0] = self.screen.get_width() / 2
            sprite.rect.center = L[0], L[1]

    def _left_click(self) -> None:
        """
        Updates sliders on left click.

        Returns:
            None
        """
        clicked_pos = pygame.mouse.get_pos()
        if self.sound_slider.back_rect.collidepoint(clicked_pos):
            self.sound_slider.click_drag(clicked_pos)
            self.s_mouse_down = True
        if self.velocity_slider.back_rect.collidepoint(clicked_pos):
            self.velocity_slider.click_drag(clicked_pos)
            self.v_mouse_down = True
