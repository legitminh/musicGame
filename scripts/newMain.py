"""
This file is the scene manager and highest level runner

1. understand code
2. rewrite the code to be more understadable
3. rework machine notes (compactify)
4. automatic song generation
    - convert mp3/wav -> machine notes
"""
from scripts.UI import *
import pygame
from typing import Callable
from screens.intro import Intro
from screens.level import Level
from screens.levelOptions import LevelOptions
from screens.menu import Menu
from screens.options import Options
from screens.outro import Outro
from scripts.interfaces import *

songs = {0: '../Musics/Hot Cross Buns.wav', 1: '../Musics/Twinkle Twinkle Little Star.wav', 2: '../Musics/Happy Birthday.wav',
         3: '../Musics/Jingle Bells.wav', 4: '../Musics/Fur Elise.wav', 5: '../Musics/La Campanella.wav'}
# required amount of stars for each level
requirements = {
    0: 0,
    1: 3,
    2: 5,
    3: 6,
    4: 7,
    5: 8
}
# requirments is max amount with normal levels availible
invrequirements = {v: k for k, v in requirements.items()}
pygame.init()
screen = pygame.display.set_mode([799, 500], pygame.RESIZABLE)

pygame.display.set_caption("Typing piano")

img = pygame.image.load('Checkered pattern.png')
pygame.display.set_icon(img)

screen.fill('dark gray')

#Game-wide critical variables
clock = pygame.time.Clock()
volume = .2
high_scores = {}


def main():
    screen_redirect: mode_type  = (Screens.intro, {})
    conversion_table = {
        Screens.menu: Menu, 
        Screens.intro: Intro, 
        Screens.option: Options, 
        Screens.level: Level, 
        Screens.outro: Outro, 
        Screens.leveOptions: LevelOptions, 
    }

    file_reader()
    while True:
        try:
            screen_redirect = conversion_table[screen_redirect[0]](screen, **screen_redirect[1]).level()
        except ExitException:
            file_writer()
            pygame.quit()
            exit()


def update_high_scores(level_num, score, slow_down):
    print(slow_down)
    if slow_down < 1:
        return 
    if str(level_num) not in high_scores:
        high_scores[str(level_num)] = score
    if score > high_scores[str(level_num)]:
        high_scores[str(level_num)] = score
    

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
