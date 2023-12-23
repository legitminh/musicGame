import pygame
from interfaces import ScreenID, ExitException
from typing import Callable
from abc import abstractmethod
from constants import FRAME_RATE


Callback = Callable[[pygame.event.Event], None]


class Screen:
    def __init__(
            self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs) -> None:
        self.screen = screen
        self.clock = clock
        self.__dict__.update(kwargs)

    @abstractmethod    
    def loop(self) -> ScreenID: ...
