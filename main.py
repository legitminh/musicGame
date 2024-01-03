"""
This file handels entering and exiting from the program.

TODO: convert mp3/wav to machine notes.
TODO: provide more support for resizing the screen.
"""
import json
import pygame
from gui.screen import Screen
from gui.intro import Intro
from gui.options import Options
from gui.menu import Menu
from gui.levelOptions import LevelOptions
from gui.level import Level
from gui.outro import Outro
from gui.UI import *
from gui.interfaces import *


pygame.init()
screen = pygame.display.set_mode([800, 500], pygame.RESIZABLE)

pygame.display.set_caption("Typing piano")

img = pygame.image.load('Assets/Images/Checkered pattern.png')
pygame.display.set_icon(img)

# Game-wide critical variables
clock = pygame.time.Clock()
high_scores: dict[str, float]
volume: float
velocity: float
bucket_settings: list[int, str]


def main():
    global high_scores, volume, velocity, bucket_settings
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
    json_reader()
    # print(bucket_settings)
    stored_kwargs = {'volume': volume, 'high_scores': high_scores, 'velocity': velocity, "bucket_settings" : bucket_settings}
    while True:
        try:
            obj: Screen = conversion_table[redirect.redirect_screen](screen, clock, **stored_kwargs)
            redirect = obj.loop()
            stored_kwargs.update(redirect.params)
        except ExitException:
            volume = stored_kwargs['volume']
            velocity = stored_kwargs['velocity']
            json_writer()
            pygame.quit()
            exit()


def json_writer():
    dictionary = {
        "playerHighScores": high_scores,
        "volume": volume,
        "velocity": velocity,
        "bucketSettings" : bucket_settings,
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    with open("playerData.json", "w") as outfile:
        outfile.write(json_object)


def json_reader():
    global high_scores, volume, velocity, bucket_settings
    with open('playerData.json', 'r') as openfile:
 
    # Reading from json file
        json_object = json.load(openfile)
        high_scores = json_object["playerHighScores"]
        volume = json_object["volume"]
        velocity = json_object["velocity"]
        bucket_settings = json_object["bucketSettings"]


if __name__ == "__main__":
    main()
