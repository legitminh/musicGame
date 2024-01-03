import pygame


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
LINE_COLOR = 'black'

NOTE_COLOR = 'black'
FILL_COLOR = 'dark gray'
FILL_COMPLETE_COLOR = 'light green'

BACKGROUND_COLOR = 'gray'
ALT_COLOR = 'dark gray'
ALT_PERIOD = 4

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

# bucket_display_order = [
#     *[96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45],
#     *[9, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91],
#     *[1073741881, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39],
#     pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT,

#     pygame.K_F1, pygame.K_F2,pygame.K_F3,pygame.K_F4,pygame.K_F5,pygame.K_F6,pygame.K_F7,pygame.K_F8,pygame.K_F9,pygame.K_F10,pygame.K_F11,pygame.K_F12,
#     pygame.K_PRINTSCREEN, pygame.K_SCROLLLOCK, pygame.K_PAUSE, pygame.K_INSERT, pygame.K_HOME, pygame.K_PAGEUP, pygame.K_DELETE, pygame.K_END, pygame.K_PAGEDOWN, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT,
#     pygame.K_NUMLOCK, pygame.K_KP_DIVIDE, pygame.K_KP_MULTIPLY, pygame.K_KP_7,  pygame.K_KP_8,  pygame.K_KP_9,  pygame.K_KP_4,  pygame.K_KP_5,  pygame.K_KP_6,  pygame.K_KP_1,  pygame.K_KP_2,  pygame.K_KP_3,
#     *[1073742048, 1073742051, 1073742050, 32, 1073742054, 1073741925, 1073742052, 1073741922, 1073741923, 1073741912, 1073741911, 1073741910]
# ]
bucket_display_order = [96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 9, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 1073741881, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 1073742049, 122, 120, 99, 118, 98, 110, 109, 44, 46, 47, 1073742053, 1073741882, 1073741883, 1073741884, 1073741885, 1073741886, 1073741887, 1073741888, 1073741889, 1073741890, 1073741891, 1073741892, 1073741893, 1073741894, 1073741895, 1073741896, 1073741897, 1073741898, 1073741899, 127, 1073741901, 1073741902, 1073741904, 1073741905, 1073741903, 1073741907, 1073741908, 1073741909, 1073741919, 1073741920, 1073741921, 1073741916, 1073741917, 1073741918, 1073741913, 1073741914, 1073741915, 1073742048, 1073742051, 1073742050, 32, 1073742054, 1073741925, 1073742052, 1073741922, 1073741923, 1073741912, 1073741911, 1073741910]
# print(bucket_display_order, len(bucket_display_order) == 8*12)
# the names of the buckets
# bucket_name_order = [
#     *"`1234567890-",
#     "Tb",*"qwertyuiop[",
#     "Cp",*"asdfghjkl;'",
#     "Ls",*"zxcvbnm,./","Rs",
#     "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",
#     "Ps","Sl","Pa","In","Ho","PgU","Del","End","PgD","<-","v|","->",
#     "Nl","N/","N*","N7","N8","N9","N4","N5","N6","N1","N2","N3",
#     "Lc","Lwi","Lal","Spc","Ral","Men","Rc","N0","N.","Nen","N+","N-"
# ]
bucket_name_order = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'Tb', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', 'Cp', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Ls', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Rs', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'Ps', 'Sl', 'Pa', 'In', 'Ho', 'PgU', 'Del', 'End', 'PgD', '<-', 'v|', '->', 'Nl', 'N/', 'N*', 'N7', 'N8', 'N9', 'N4', 'N5', 'N6', 'N1', 'N2', 'N3', 'Lc', 'Lwi', 'Lal', 'Spc', 'Ral', 'Men', 'Rc', 'N0', 'N.', 'Nen', 'N+', 'N-']
# BUCKET_CODE_TO_DISPLAY = {
#     bucket_display_order[i]:bucket_name_order[i] for i in range(len(bucket_display_order))
# }
BUCKET_CODE_TO_DISPLAY = {96: '`', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 48: '0', 45: '-', 9: 'Tb', 113: 'q', 119: 'w', 101: 'e', 114: 'r', 116: 't', 121: 'y', 117: 'u', 105: 'i', 111: 'o', 112: 'p', 91: '[', 1073741881: 'Cp', 97: 'a', 115: 's', 100: 'd', 102: 'f', 103: 'g', 104: 'h', 106: 'j', 107: 'k', 108: 'l', 59: ';', 39: "'", 1073742049: 'Ls', 122: 'z', 120: 'x', 99: 'c', 118: 'v', 98: 'b', 110: 'n', 109: 'm', 44: ',', 46: '.', 47: '/', 1073742053: 'Rs', 1073741882: 'F1', 1073741883: 'F2', 1073741884: 'F3', 1073741885: 'F4', 1073741886: 'F5', 1073741887: 'F6', 1073741888: 'F7', 1073741889: 'F8', 1073741890: 'F9', 1073741891: 'F10', 1073741892: 'F11', 1073741893: 'F12', 1073741894: 'Ps', 1073741895: 'Sl', 1073741896: 'Pa', 1073741897: 'In', 1073741898: 'Ho', 1073741899: 'PgU', 127: 'Del', 1073741901: 'End', 1073741902: 'PgD', 1073741904: '<-', 1073741905: 'v|', 1073741903: '->', 1073741907: 'Nl', 1073741908: 'N/', 1073741909: 'N*', 1073741919: 'N7', 1073741920: 'N8', 1073741921: 'N9', 1073741916: 'N4', 1073741917: 'N5', 1073741918: 'N6', 1073741913: 'N1', 1073741914: 'N2', 1073741915: 'N3', 1073742048: 'Lc', 1073742051: 'Lwi', 1073742050: 'Lal', 32: 'Spc', 1073742054: 'Ral', 1073741925: 'Men', 1073742052: 'Rc', 1073741922: 'N0', 1073741923: 'N.', 1073741912: 'Nen', 1073741911: 'N+', 1073741910: 'N-'}

# BUCKET_ID_TO_CODE = {
#     f"{str(i)}": [int(j), f"{str(k)}"] for i, (j,k) in enumerate(BUCKET_CODE_TO_DISPLAY.items())
# }

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
