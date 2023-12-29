"""
This file handels entering and exiting from the program.

TODO: convert mp3/wav to machine notes.
TODO: provide more support for resizing the screen.
"""

import pygame
from screens.screen import Screen
from screens.intro import Intro
from screens.options import Options
from screens.menu import Menu
from screens.levelOptions import LevelOptions
from screens.level import Level
from screens.outro import Outro
from UI import *
from interfaces import *


pygame.init()
screen = pygame.display.set_mode([800, 500], pygame.RESIZABLE)

pygame.display.set_caption("Typing piano")

img = pygame.image.load('Assets/Images/Checkered pattern.png')
pygame.display.set_icon(img)

screen.fill('dark gray')

# Game-wide critical variables
clock = pygame.time.Clock()
volume = .2  # TODO: store volume inside of player data
high_scores: dict[str, float] = {}


def main():
    """Handels screen redirects and stores the player's scores"""
    redirect: Redirect = Redirect(ScreenID.intro)
    conversion_table: dict[ScreenID, Screen] = {
        ScreenID.intro:        Intro,        # Kwargs: None
        ScreenID.option:       Options,      # Kwargs: volume
        ScreenID.menu:         Menu,         # Kwargs: high_scores
        ScreenID.levelOptions: LevelOptions, # Kwargs: high_scores, song_id
        ScreenID.level:        Level,        # Kwargs: volume, song_id, slowdown
        ScreenID.outro:        Outro,        # Kwargs: song_id, score, slowdown, high_scores
    }
    stored_kwargs = {'volume': volume, 'high_scores': high_scores}

    file_reader()
    while True:
        try:
            obj: Screen = conversion_table[redirect.redirect_screen](screen, clock, **stored_kwargs)
            redirect = obj.loop()
            stored_kwargs.update(redirect.params)
        except ExitException:
            file_writer()
            pygame.quit()
            exit()


def file_writer() -> None: 
    """Saves high scores into the `PlayerData` file."""
    with open('PlayerData', mode='w') as f:
        write = ''
        for level_n, percent in high_scores.items():
            write += f'{level_n},{percent}\n'
        f.write(write)


def file_reader() -> None:
    """Reads high scores from the `PlayerData` file."""
    global high_scores
    with open('PlayerData', mode='r') as f:
        for line in f.read().strip().split():
            high_scores[line.split(',')[0]] = float(line.split(',')[1])


if __name__ == "__main__":
    main()
