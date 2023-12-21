"""
This file is the scene manager and highest level runner

1. understand code
2. rewrite the code to be more understadable
3. rework machine notes (compactify)
4. automatic song generation
    - convert mp3/wav -> machine notes
"""

import pygame
from screens.intro import Intro
from screens.level import Level
from screens.levelOptions import LevelOptions
from screens.menu import Menu
from screens.options import Options
from screens.outro import Outro
from UI import *
from interfaces import *


pygame.init()
screen = pygame.display.set_mode([799, 500], pygame.RESIZABLE)

pygame.display.set_caption("Typing piano")

img = pygame.image.load('Assets/Checkered pattern.png')
pygame.display.set_icon(img)

screen.fill('dark gray')

#Game-wide critical variables
clock = pygame.time.Clock()
volume = .2
high_scores = {}


def main():
    screen_redirect: ScreenID = ScreenID.intro
    conversion_table: dict[ScreenID, Screen] = {
        ScreenID.intro:        Intro,        # Kwargs: None
        ScreenID.option:       Options,      # Kwargs: volume
        ScreenID.menu:         Menu,         # Kwargs: high_scores
        ScreenID.levelOptions: LevelOptions, # Kwargs: high_scores, song_id
        ScreenID.level:        Level,        # Kwargs: volume, song_id, slowdown
        ScreenID.outro:        Outro,        # Kwargs: song_id, score, slowdown, high_scores
    }
    TARGET_KWARGS = ['volume', 'high_scores', 'song_id', 'slowdown', 'score']
    stored_kwargs = {'volume': volume, 'high_scores': high_scores}

    file_reader()
    while True:
        try:
            obj: Screen = conversion_table[screen_redirect](screen, clock, **stored_kwargs)
            screen_redirect = obj.loop()
            for key in obj.__dict__:
                if key in TARGET_KWARGS:
                    stored_kwargs[key] = obj.__dict__[key]
        except ExitException:
            file_writer()
            pygame.quit()
            exit()


def file_writer() -> None: #save notes into file 
    with open('PlayerData', mode='w') as f:
        write = ''
        for level_n, percent in high_scores.items():
            write += f'{level_n},{percent}\n'
        f.write(write)


def file_reader():
    global high_scores
    with open('PlayerData', mode='r') as f:
        for line in f.read().strip().split():
            high_scores[line.split(',')[0]] = float(line.split(',')[1])


if __name__ == "__main__":
    main()
