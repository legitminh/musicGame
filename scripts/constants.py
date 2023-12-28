FRAME_RATE = 50
FONT_PATH = "Assets/Fonts/Roboto-Light.ttf"
# Musics\Fur Elise.wav
SONG_PATHS = {0: 'Musics/Hot Cross Buns.wav', 1: 'Musics/Twinkle Twinkle Little Star.wav', 2: 'Musics/Happy Birthday.wav',
         3: 'Musics/Jingle Bells.wav', 4: 'Musics/Fur Elise.wav', 5: 'Musics/La Campanella.wav', 6: 'Musics/Rush E.wav'}

# required amount of stars for each level
REQUIREMENTS = {
    0: 0,
    1: 5,
    2: 10,
    3: 15,
    4: 20,
    5: 25,
    6: 30,
    7: 35,
    8: 40,
    9: 45,
}

SCORE2STARS = {
    60: 0,  # up to and including 60: 0 stars
    70: 1,
    80: 2,
    90: 3,
    95: 4,
    100: 5,
    160: 6,
    170: 7,
    180: 8,
    190: 9,
    200: 10,
}

# requirments is max amount with normal levels availible
INVREQUIREMENTS = {v: k for k, v in REQUIREMENTS.items()}
