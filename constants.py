FRAME_RATE = 50
FONT_PATH = "Assets/Fonts/Roboto-Light.ttf"
SONG_PATHS = {
    0: 'Musics/Hot Cross Buns.wav', 
    1: 'Musics/Twinkle Twinkle Little Star.wav', 
    2: 'Musics/Mary Had a Little Lamb.wav',
    3: 'Musics/Happy Birthday.wav',
    4: 'Musics/Jingle Bells.wav', 
    5: "Musics/Canon in D Piano.wav", 
    6: 'Musics/Fur Elise.wav', 
    7: 'Musics/La Campanella.wav', 
    8: 'Musics/Rush E.wav'
}

LENIENCY = 0.5  # seconds
LINE_LEVEL = 0.8

NOTE_COLOR = 'black'
FILL_COLOR = 'dark gray'
FILL_COMPLETE_COLOR = 'light green'

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
