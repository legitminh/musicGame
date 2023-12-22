import pygame
from interfaces import ScreenID, ExitException
from typing import Callable
from abc import abstractmethod
from constants import FRAME_RATE


def _quit(event): raise ExitException()
def _key_down(event):
    if event.key == pygame.K_ESCAPE:
        raise ExitException


Callback = Callable[[pygame.event.Event], None]


class Screen:
    def __init__(
            self, screen: pygame.Surface, clock: pygame.time.Clock, 
            event_functions: dict[int, Callback]=None, **kwargs) -> None:
        self.screen = screen
        self.clock = clock
        
        self.event_functions = {
            pygame.QUIT: _quit,
            pygame.KEYDOWN: _key_down,
        }
        if event_functions is not None:
            self.event_functions.update(event_functions)
        
        self.__dict__.update(kwargs)
    
    def loop(self) -> ScreenID:
        self._set_up()
        while True:
            for event in pygame.event.get():
                if event.type in self.event_functions:
                    # run the function
                    self.event_functions[event]()
            self._draw()
            self.clock.tick(FRAME_RATE)
            pygame.display.update()

    @abstractmethod
    def _draw(self) -> None: ...

    @abstractmethod
    def _set_up(self) -> None: ...
