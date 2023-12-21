FRAME_RATE = 50
# Musics\Fur Elise.wav
SONGS = {0: 'Musics/Hot Cross Buns.wav', 1: 'Musics/Twinkle Twinkle Little Star.wav', 2: 'Musics/Happy Birthday.wav',
         3: 'Musics/Jingle Bells.wav', 4: 'Musics/Fur Elise.wav', 5: 'Musics/La Campanella.wav'}

# required amount of stars for each level
REQUIREMENTS = {
    0: 0,
    1: 3,
    2: 5,
    3: 6,
    4: 7,
    5: 8
}

# requirments is max amount with normal levels availible
INVREQUIREMENTS = {v: k for k, v in REQUIREMENTS.items()}
