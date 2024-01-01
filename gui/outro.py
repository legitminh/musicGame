"""
This file handels displaying the outro screen.
"""
import pygame
from .interfaces import *
from .UI import Button
from .screen import Screen
from constants import *

class Outro(Screen):
    """
    This class handels displaying the outro and player interactions.
    """
    high_scores: dict[str, float]
    slowdown: float
    score: float

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs) -> None:
        """
        Creates the outro object.

        Args:
            screen (pygame.Surface): The surface that the level object will draw itself on.
            clock (pygame.time.Clock): The clock which will be used to set the maximum fps.
            **kwargs (Any): Any other arguments, will ignore all values other than `song_id`, `score`, `slowdown`, and `high_scores`.
                song_id (int): The id of the song that will be played.
                score (float): The score of the player.
                slowdown (int | float): The amount the song will be slow downed 
                    (will run the pre-slow-downed version of the song located in the "ProcessedMusics" directory)
                high_scores (dict[str, float]): The high scores of the player.
        
        Returns:
            None

        Raises:
            ValueError: If `song_id`, `score`, `slowdown`, or `high_scores` are not in `kwargs`.
        """
        tmp = kwargs.copy()
        arguments = {'song_id': int, 'score': float, 'slowdown': int | float, 'high_scores': dict}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        
        kwargs = tmp
        for arg, arg_type in arguments.items():
            if arg not in kwargs or not isinstance(kwargs[arg], arg_type):
                print(arg)
                raise ValueError("Key word argument not included or is of an unacceptable type.")
        
        super().__init__(screen, clock, **kwargs)
        self._buttons_init()

    def loop(self) -> None:
        """
        The main game loop.

        Returns:
            Redirect: A screen redirect.
        
        Raises:
            ExitException: If the user exits out of the screen.
        """
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

    def _buttons_init(self) -> None:
        """
        Initializes the buttons.

        Returns:
            None
        """
        self.outro_g = pygame.sprite.Group()
        if isinstance(self.song_id, str):
            directory = SONG_PATHS[int(self.song_id.replace('e', '').replace('p', ''))]
        else:
            directory = SONG_PATHS[self.song_id]
        
        self.outro_l = [Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 + 50], self.song_id, 'Play again', 30),
                Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 - 50], '',
                        f'You scored {self.score:.2f}% on {directory[directory.find("/") + 1:directory.find(".")]}',
                        30),
                Button(self.screen, [self.screen.get_width() / 2, self.screen.get_height() // 2 + 110], ScreenID.menu,
                        'Return to level selection', 30)]
        self.outro_g.add(self.outro_l)

    def _draw(self) -> None:
        """
        Draws all elements onto the screen.

        Returns:
            None
        """
        self.screen.fill('light gray')
        self.outro_g.draw(self.screen)
        self.outro_g.update()
        pygame.display.update()

    def _button_clicked(self) -> None:
        """
        Updates the button based on button click location.

        Returns:
            None
        """
        pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.outro_g.sprites()):
            if not sprite.rect.collidepoint(*pos):
                continue
            if not (isinstance(self.outro_l[i].mode_c, int) or self.outro_l[i].mode_c):
                break
            if isinstance(self.outro_l[i].mode_c, str | int):
                return Redirect(ScreenID.level, song_id=self.outro_l[i].mode_c)
            return Redirect(self.outro_l[i].mode_c)

    def _update_high_scores(self) -> None:
        """
        Updates the high scores of the players.

        Returns:
            None
        """
        if self.slowdown < 1:
            return 
        if str(self.song_id) not in self.high_scores:
            self.high_scores[str(self.song_id)] = self.score
            return
        if self.score > self.high_scores[str(self.song_id)]:
            self.high_scores[str(self.song_id)] = self.score
