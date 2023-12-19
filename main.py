"""
TODO:
 - write more levels / create a program that will help you write levels
 - The length of the note effects point scoring, the shorter the less value, the longer the more value

# the below will never happen
A login screen
Sound effects
Animation
Images
Cross platform compatibility
"""
from UIclasses import *
import pygame
import soundfile as sf
from random import choice
from sys import exit as end

songs = {0: 'Musics/Hot Cross Buns.wav', 1: 'Musics/Twinkle Twinkle Little Star.wav', 2: 'Musics/Happy Birthday.wav',
         3: 'Musics/Jingle Bells.wav', 4: 'Musics/Fur Elise.wav', 5: 'Musics/La Campanella.wav'}
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
clock = pygame.time.Clock()
volume = .2
high_scores = {}


def main():
    mode = "intro"
    file_reader()
    while True:  # Playing >> End screen
        if mode == "intro":
            mode = intro()
        elif mode == 'level selection':
            mode = level_select()
        elif mode == 'options':
            mode = options()
        elif isinstance(mode, int):
            mode = mode_choice(str(mode))
            try:
                slowdown = float(mode[1])
            except ValueError:
                continue
            if isinstance(mode[0], int):
                mode = level(mode[0], mode[1])
            elif 'e' in mode[0]:
                mode = extreme_level(int(mode[0].replace('e', '')), mode[1])
            if isinstance(mode, tuple) and slowdown < .006:
                try:
                    if mode[1] > high_scores[str(mode[0])]:
                        high_scores[str(mode[0])] = float(f'{mode[1]:.5f}')
                except KeyError:
                    high_scores[str(mode[0])] = mode[1]
        elif isinstance(mode, tuple):
            mode = outro(mode)


def intro():
    while True:
        intro_g = pygame.sprite.Group()
        intro_l = [
            Button(screen, [screen.get_width() // 2, screen.get_height() // 2 - 50], '', 'Typing Piano', 50),
            Button(screen, [screen.get_width() // 2, screen.get_height() // 2 + 50], 'level selection', 'Play', 30),
            Button(screen, [screen.get_width() // 2, screen.get_height() // 2 + 100], 'options', 'Options', 30)
        ]
        intro_g.add(intro_l)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_writer()
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    file_writer()
                    pygame.quit()
                    end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(intro_g.sprites())):
                        s = intro_g.sprites()[i]
                        pos = pygame.mouse.get_pos()
                        if s.rect.collidepoint(pos[0], pos[1]) and intro_l[i].mode_c:
                            return intro_l[i].mode_c
        screen.fill('light gray')
        intro_g.draw(screen)
        intro_g.update()
        pygame.display.update()


def options():
    global volume
    sound_slider = ScrollBar(screen, [25, 160], [screen.get_width() - 25, 180], [50, 20], 'black', 'dark gray',
                             orientation='horizontal', start_pos=[50 + (volume * (screen.get_width() - 150)), 160])
    sliders = pygame.sprite.Group(sound_slider)
    user_interfaces = [
        Button(screen, [screen.get_width() / 2, 50], '', 'Options', 50),
        Button(screen, [screen.get_width() / 2, 125], '', 'Volume', 30)
    ]
    others = pygame.sprite.Group(user_interfaces)
    mouse_down = False
    while True:
        screen.fill('light gray')
        volume = int(sound_slider.rect.topleft[0] - sound_slider.start_pos[0]) / (
                    sound_slider.end_pos[0] - sound_slider.start_pos[0] - sound_slider.rect.width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_writer()
                pygame.quit()
                end()
            elif event.type == pygame.VIDEORESIZE:
                sound_slider.end_pos = screen.get_width() - 25, 180
                sound_slider.update(screen_change=True)
                leng = sound_slider.end_pos[0] - sound_slider.start_pos[0] - sound_slider.rect.width
                sound_slider.rect.topleft = sound_slider.start_pos[0] + (volume * leng), 160
                for sprite in user_interfaces:
                    L = list(sprite.rect.center)
                    L[0] = screen.get_width() / 2
                    sprite.rect.center = L[0], L[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = pygame.mouse.get_pos()
                    if sound_slider.back_rect.collidepoint(clicked_pos):
                        sound_slider.click_drag(clicked_pos)
                        mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "intro"
        if mouse_down:
            sound_slider.click_drag(pygame.mouse.get_pos())
        sliders.update(f'{int(volume * 100)}%', args_c='white')
        others.draw(screen)
        others.update()
        pygame.display.update()


def level_select():
    # high score
    level_amount = 10
    up = 0
    high_score_g = pygame.sprite.Group()
    high_score_l = []
    for _i in range(level_amount):
        try:
            name = high_scores[str(_i)]
        except KeyError:
            name = 0
        high_score_l.append(
            Button(screen, [screen.get_width() - 100, _i * 60 + 95 - up], _i, int(name), 30, alignment_pos='topright')
        )
    high_score_g.add(high_score_l)
    # star
    stars_g = pygame.sprite.Group()
    stars_l = []
    stars = 0
    for _i in range(level_amount):
        try:
            if 0 <= high_scores[str(_i)] < 50:
                star = 0
            elif high_scores[str(_i)] < 75:
                star = 1
            elif high_scores[str(_i)] < 90:
                star = 2
            elif high_scores[str(_i)] < 100:
                star = 3
            else:
                star = 5
        except KeyError:
            star = 0
        try:
            _i = str(_i) + 'e'
            if 0 <= high_scores[str(_i)] < 50:
                star += 0
            elif high_scores[str(_i)] < 75:
                star += 1
            elif high_scores[str(_i)] < 90:
                star += 2
            elif high_scores[str(_i)] < 100:
                star += 3
            else:
                star += 5
        except KeyError:
            star += 0
        stars += star
        _i = int(_i.replace('e', ''))
        stars_l.append(
            Button(screen, [screen.get_width(), _i * 60 + 95 - up], '', star, 30, path='Assets/star.png',
                   dim=(59, 59), alignment_pos='topright')
        )
    stars_g.add(stars_l)
    # screen title and stars N
    others_g = pygame.sprite.Group()
    others_l = [
        Button(screen, [screen.get_width() / 2, 50], '', 'Click On a Level', 50),
        Button(screen, [screen.get_width(), 10], '', stars, 50, alignment_pos='topright')
    ]
    others_g.add(others_l)
    # songs and locks display
    level_select_g = pygame.sprite.Group()
    level_select_l = []
    lock_g = pygame.sprite.Group()
    lock_l = []
    for _i in range(level_amount):
        try:  # if song is written
            locked = requirements[_i] > stars
            directory = songs[_i]
            if locked:
                lock_l.append(Button(screen, [10, _i * 60 + 95 - up], '', requirements[_i], 30, alignment_pos='topleft',
                                     path='Assets/lock.png', dim=(59, 59)))
        except KeyError:  # if song doesn't exist
            locked = True
            directory = "/0."
        name = directory[directory.find("/") + 1:directory.find(".")]
        level_select_l.append(
            Button(screen, [100, _i * 60 + 95 - up], '' if locked else _i, name, 30, alignment_pos='topleft'))
    lock_g.add(lock_l)
    level_select_g.add(level_select_l)
    # slider
    slider = ScrollBar(screen, [0, 100], [10, screen.get_height()], [10, 50], 'black', 'dark gray')
    slider_g = pygame.sprite.GroupSingle(slider)
    velocity = 0
    last_time = pygame.time.get_ticks()
    total_len = level_select_l[-1].rect.bottom - level_select_l[0].rect.top - screen.get_height() + 100
    index = 1 if slider.orientation == 'vertical' else 0
    slider_step_size = (slider.end_pos[index] - slider.start_pos[index] - slider.dim[index]) / total_len
    slider.step_size = slider_step_size
    level_select_g.add(level_select_l)
    mouse_down = False
    framerate = 30
    while True:
        dt = (pygame.time.get_ticks() - last_time) / 1000
        dt *= 60
        last_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_writer()
                pygame.quit()
                end()
            elif event.type == pygame.VIDEORESIZE:
                slider.end_pos = [10, screen.get_height()]
                slider.update(screen_change=True)
                total_len = level_select_l[-1].rect.bottom - level_select_l[0].rect.top - screen.get_height() + 100
                index = 1 if slider.orientation == 'vertical' else 0
                slider_step_size = (slider.end_pos[index] - slider.start_pos[index] - slider.dim[index]) / total_len
                slider.step_size = slider_step_size
                others_l[0].rect.center = [screen.get_width() / 2, 50]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'intro'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = pygame.mouse.get_pos()
                    for i in range(len(level_select_g.sprites())):
                        s = level_select_g.sprites()[i]
                        if s.rect.collidepoint(clicked_pos) and isinstance(level_select_l[i].mode_c, int):
                            return level_select_l[i].mode_c
                    if slider.back_rect.collidepoint(clicked_pos):
                        mouse_down = True
                        up = slider.click_drag(clicked_pos)
                elif event.button == 4:
                    velocity -= dt * 4
                elif event.button == 5:
                    velocity += dt * 4
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
        if mouse_down:
            up = slider.click_drag(pygame.mouse.get_pos())
        if total_len > 0:
            velocity *= .9
            if abs(velocity) < 1:
                velocity = 0
            up += velocity
            if up < 0:
                up = 0
                velocity = 0
            elif up > total_len:
                up = total_len
                velocity = 0
            slider.rect.topleft = slider.rect.topleft[0], up * slider_step_size + slider.start_pos[1]
        else:
            up = 0
        for i, sprite in enumerate(level_select_l):
            sprite.set_pos((84, i * 60 + 95 - up))
        width = screen.get_width()
        for i, sprite in enumerate(high_score_l):
            sprite.set_pos((width - 100, i * 60 + 95 - up))
        for i, sprite in enumerate(stars_l):
            sprite.set_pos((width - 40, i * 60 + 93 - up))
        for i, sprite in enumerate(lock_l):
            sprite.set_pos((15, invrequirements[int(sprite.text)] * 60 + 95 - up))
        screen.fill('light gray')
        height = screen.get_height()
        to_draw = pygame.sprite.Group()
        for sprite in level_select_g.sprites() + high_score_g.sprites() + stars_g.sprites() + lock_g.sprites():
            if height > sprite.rect.top and sprite.rect.bottom > 95:
                to_draw.add(sprite)
        to_draw.draw(screen)
        to_draw.update()
        pygame.draw.rect(screen, 'light gray', (0, 0, width, 95))
        others_g.draw(screen)
        others_g.update()
        if total_len > 0:
            slider_g.update()
            slider_g.draw(screen)
        pygame.display.update()
        clock.tick(framerate)


def mode_choice(which):
    # modes
    modes_l = [
        Button(screen, [screen.get_width() / 2, screen.get_height() / 2 - 130], '', 'Speed', 30),
        Button(screen, [screen.get_width() / 2 - 105, screen.get_height() / 2 - 65], '.75', '75%', 30),
        Button(screen, [screen.get_width() / 2, screen.get_height() / 2 - 65], '.50', '50%', 30),
        Button(screen, [screen.get_width() / 2 + 105, screen.get_height() / 2 - 65], '.25', '25%', 30),
        Button(screen, [screen.get_width() / 2, screen.get_height() / 2], int(which), 'Normal', 30),
        Button(screen, [screen.get_width() / 2, screen.get_height() / 2 + 65], which + 'e', 'Extreme', 30)
    ]
    modes_g = pygame.sprite.Group()
    modes_g.add(modes_l)
    # lock
    lock_g = pygame.sprite.GroupSingle()
    if high_scores[which] != 100:
        lock_g.add(Button(screen, modes_l[5].rect.center, '', 0, 0, path='Assets/lock.png',
                          dim=(50, 50), alignment_pos='center'))
    framerate = 20
    slow_down = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                end()
            elif event.type == pygame.VIDEORESIZE:
                for i, button in enumerate(modes_l):
                    # button.rect.center = screen.get_width() / 2, screen.get_height() / 2 + 65
                    screen.get_width() / 2, screen.get_height() / 2 + 50 * (i - 1) - (0 if i else 65)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'level selection'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = pygame.mouse.get_pos()
                    for i in range(len(modes_g.sprites())):
                        if modes_g.sprites()[i].rect.collidepoint(clicked_pos):
                            if '.' in str(modes_l[i].mode_c):
                                if float(modes_l[i].mode_c) == slow_down:
                                    slow_down = 1
                                    modes_l[i].color_changer((150, 150, 150, 255))
                                else:
                                    for sprite in modes_l[1:4]:
                                        sprite.color_changer((150, 150, 150, 255))
                                    slow_down = float(modes_l[i].mode_c)
                                    modes_l[i].color_changer((0, 150, 0, 255))
                                break
                            if 'e' in str(modes_l[i].mode_c) and high_scores[which] == 100:
                                return modes_l[i].mode_c, slow_down
                            elif 'e' not in str(modes_l[i].mode_c) and (modes_l[i].mode_c or modes_l[i].mode_c == 0):
                                return modes_l[i].mode_c, slow_down
        screen.fill('light gray')
        modes_g.draw(screen)
        modes_g.update()
        if high_scores[which] != 100:
            lock_g.draw(screen)
            lock_g.update()
        pygame.display.update()
        clock.tick(framerate)


def extreme_level(which, slowdown) -> tuple[str, float] | str:
    colors = [(255, 0, 0, 100), (255, 165, 0, 100), (255, 255, 0, 100), (0, 255, 0, 100), (0, 255, 255, 100),
              (0, 0, 255, 100), (255, 0, 255, 100)]
    note_change = {
        'q': '1qaz',
        'w': '2wsx',
        'e': '3edc',
        'r': '4rfv',
        't': '5tgb',
        'y': '8uhy',
        'u': '9ijn',
        'i': '0okm',
        'o': '-pl,',
        'p': '=[;.',
    }
    note_numbers = {} #option and their collum number(x postion)
    note_rep = {} #rank placement up down of key board
    holds: dict[str, None | float] = {
    }
    for a, (k, options) in enumerate(note_change.items()):
        for rank, option in enumerate(options):
            holds[option] = None
            note_numbers[option] = a
            note_rep[option] = rank

    dt = 0
    notes = note_extractor(which, slowdown)
    for i, note in enumerate(notes):
        note[0] = choice(note_change[note[0]])
    correct_hits = 0
    total_hits = 0
    last_time = pygame.time.get_ticks()
    framerate = 50
    first = True
    pygame.mixer.music.set_volume(volume)

    # noinspection PyTypeChecker
    def all_note_cycle():  # note GFX
        nonlocal notes
        current_color = 0
        notes_copy = notes[:]
        notes_copy.reverse()
        for note in notes_copy:  # check list representing note
            if note[2] <= 0 <= note[2] + note[1]:
                color = (0, 255, 0, 255)  # green-clickable
            else:
                color = colors[current_color]
                current_color += 1
                if current_color == len(colors):
                    current_color = 0
            if holds[note[0]] == 0 and note[2] <= 0 <= note[2] + note[1] and note[3]:
                color = (255, 0, 0, 255)
            draw_rect_alpha(screen, color, (
                note_numbers[note[0]] * screen.get_width() / 10, screen.get_height() * .8 - note[2] - note[1],
                screen.get_width() / 10, note[1]))
            note[2] -= dt  # decrease time>>note fall down.
    
    def draw_key_rank():
        width = screen.get_width()
        height = screen.get_height()
        for note in notes:
            if note_rep[note[0]] != 0:
                if height * .8 - note[2] - note[1]/2 - 8 < 0:
                    break
                screen.blit(pygame.image.load(f"Assets/Extreme/{note_rep[note[0]]}.png"),
                (note_numbers[note[0]] * width / 10+ width / 20-8,
                 height * .8 - note[2] - note[1]/2 - 8))
    
    def draw_key_names():
        width = screen.get_width()
        height = screen.get_height()
        lowest: list[int] = []
        for note in notes:
            if note_numbers[note[0]] in lowest:
                continue
            if len(lowest) == 10:
                return
            lowest.append(note_numbers[note[0]])
            make_text(note_numbers[note[0]] * width / 10 + width / 20, height * .9, note[0])

    while True:
        line_level = int(screen.get_height() * .8)
        screen.fill('dark gray')
        pygame.draw.line(screen, 'black', (0, line_level), (screen.get_width(), line_level))
        dt = (pygame.time.get_ticks() - last_time) / 1000
        dt *= 60
        if first: dt = 0
        last_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_writer()
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return 'level selection'
                if first:
                    if slowdown < .99:
                        pygame.mixer.music.load(
                            songs[which].replace("Musics/", "ProcessedMusics/").replace(".wav", f'{int(slowdown * 100)}.wav'))
                    else:
                        pygame.mixer.music.load(songs[which])
                    pygame.mixer.music.play()
                    first = False
                clicked = False
                for i in notes:  # i = note
                    if i[2] <= 0 <= i[2] + i[1]:  # if key in range
                        if event.key == ord(i[0]):  # the target note is held
                            clicked = True
                            if i[3]:
                                holds[i[0]] = i[1] * .75
                            else:
                                notes.remove(i)
                                total_hits += 1
                                correct_hits += 1
                    else:  # it is a note that is not the lowest so don't check the rest
                        break
                if not clicked and event.key in range(97, 123):
                    total_hits += 1
            elif event.type == pygame.KEYUP:
                for i in notes:
                    if i[2] <= 0 <= i[2] + i[1] and i[3]:  # if in colliding range
                        try:  #
                            if event.key in range(97, 122) and holds[i[0]] <= 0 and i[3]:
                                total_hits += 1
                                correct_hits += 1
                                holds[i[0]] = None
                                notes.remove(i)
                        except Exception as e:
                            if isinstance(e, TypeError):
                                print(e, i, holds)
        for a in holds.keys():
            if type(holds[a]) is float:  # is being held
                if holds[a] > 0:
                    holds[a] -= dt
                else:
                    holds[a] = 0
        for i, note in enumerate(notes[:]):
            if note[2] + note[1] >= 0: # don't remove
                break
            total_hits += 1
            holds[note[0]] = None
            notes.pop(0)
        if len(notes) == 1: # if only 1 note left
            if int(notes[0][2] + notes[0][1]) < 0:
                pass
                #remove_to = 1
        # for note in notes[:remove_to]:
        #     total_hits += 1
        #     holds[note[0]] = None
        #notes = notes[remove_to:]
        if len(notes) == 0:  # check if finished song
            pygame.mixer.music.stop()
            try:
                return str(which) + 'e', correct_hits / total_hits * 100
            except ZeroDivisionError:
                return 0
        
        all_note_cycle()
        draw_key_names()
        draw_key_rank()
        try:
            make_text(screen.get_width() / 2, 20, int(correct_hits / total_hits * 100))
        except ZeroDivisionError:
            make_text(screen.get_width() / 2, 20, 0)
        pygame.display.update()
        clock.tick(framerate)


# noinspection PyTypeChecker
def level(which, slowdown) -> tuple[int, float] | str:
    colors = [(255, 0, 0, 100), (255, 165, 0, 100), (255, 255, 0, 100), (0, 255, 0, 100), (0, 255, 255, 100),
              (0, 0, 255, 100),
              (255, 0, 255, 100)]
    note_numbers = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9}
    keys = {'q': 113, 'w': 119, 'e': 101, 'r': 114, 't': 116, 'y': 121, 'u': 117, 'i': 105, 'o': 111,
            'p': 112}
    holds: dict[str, None | float] = {'q': None, 'w': None, 'e': None, 'r': None, 't': None, 'y': None,
                                      'u': None, 'i': None, 'o': None, 'p': None}
    dt = 0
    notes = note_extractor(which, slowdown)
    correct_hits = 0
    total_hits = 0
    last_time = pygame.time.get_ticks()
    framerate = 50
    first = True
    holding = {'q': False, 'w': False, 'e': False, 'r': False, 't': False, 'y': False,
                                      'u': False, 'i': False, 'o': False, 'p': False}
    pygame.mixer.music.set_volume(volume)
    # noinspection PyTypeChecker
    def all_note_cycle():  # note GFX
        nonlocal notes
        current_color = 0
        notes_copy = notes[:]
        notes_copy.reverse()
        for note in notes_copy:  # check list representing note
            if note[2] <= 0 <= note[2] + note[1]:
                color = (0, 255, 0, 255)  # green-clickable
            else:
                color = colors[current_color]
                current_color += 1
                if current_color == len(colors):
                    current_color = 0
            try:
                if holds[note[0]] == 0 and note[2] <= 0 <= note[2] + note[1] and note[3]:
                    color = (255, 0, 0, 255)
            except Exception:
                return Exception
            draw_rect_alpha(screen, color, (
                note_numbers[note[0]] * screen.get_width() / 10, screen.get_height() * .8 - note[2] - note[1],
                screen.get_width() / 10, note[1]))
            note[2] -= dt  # decrease time>>note fall down.
    
    while True:
        line_level = int(screen.get_height() * .8)
        screen.fill('gray')
        pygame.draw.line(screen, 'black', (0, line_level), (screen.get_width(), line_level))
        dt = (pygame.time.get_ticks() - last_time) / 1000 * 60
        if first: dt = 0
        last_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_writer()
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #ESC to exit song
                    pygame.mixer.music.stop()
                    return 'level selection'
                if first:
                    if slowdown < .99:
                        pygame.mixer.music.load(songs[which].replace("Musics/","ProcessedMusics/").replace(".wav",f'{int(slowdown * 100)}.wav'))
                    else:
                        pygame.mixer.music.load(songs[which])
                    pygame.mixer.music.play()
                    last_time = pygame.time.get_ticks()
                    first = False
                clicked = False
                for i in notes:  # i = note
                    if i[2] <= 0 <= i[2] + i[1]:  # if key in range
                        if event.key == keys[i[0]]:  # the target note is held
                            clicked = True
                            if i[3]:
                                holds[i[0]] = i[1] * .5
                            else:
                                notes.remove(i)
                                total_hits += 1
                                correct_hits += 1
                    else:  # it is a note that is not the lowest so don't check the rest
                        break 
                if not clicked and event.key != pygame.K_SPACE:
                    # print('failure')
                    total_hits += 1
            elif event.type == pygame.KEYUP:
                for i in notes:
                    if i[2] <= 0 <= i[2] + i[1] and i[3]:  # if in colliding range
                        try:  #
                            if event.key in range(97, 122) and holds[i[0]] <= 0 and i[3]:
                                total_hits += 1
                                correct_hits += 1
                                holds[i[0]] = None
                                notes.remove(i)
                        except Exception as e:
                            if isinstance(e, TypeError):
                                print(e, i, holds)
        if len(notes) == 0:  # check if finished song
            pygame.mixer.music.stop()
            try:
                return which, correct_hits / total_hits * 100
            except ZeroDivisionError:
                return 0
        for i, note in enumerate(notes[:]):
            if note[2] + note[1] >= 0: # don't remove
                break
            total_hits += 1
            holds[note[0]] = None
            notes.pop(0)
        for a in holds.keys():
            if type(holds[a]) is float:  # is being held
                if holds[a] > 0:
                    holds[a] -= dt
                else:
                    holds[a] = 0
        all_note_cycle()
        for i in ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']:
            make_text((note_numbers[i] + .5) * screen.get_width() / 10, screen.get_height() * .9, i.upper())
        try:
            make_text(screen.get_width() / 2, 20, int(correct_hits / total_hits * 100))
        except ZeroDivisionError:
            make_text(screen.get_width() / 2, 20, 0)
        pygame.display.update()
        clock.tick(framerate)


def outro(variables):  # variable = [level number, score]
    outro_g = pygame.sprite.Group()
    if isinstance(variables[0], str):
        variables = int(variables[0].replace('e', '').replace('p', '')), variables[1]
    if isinstance(variables[0], str):
        copy = variables[0]
        copy.replace('e', '')
        directory = songs[copy]
    else:
        directory = songs[variables[0]]
    outro_l = [Button(screen, [screen.get_width() / 2, screen.get_height() // 2 + 50], variables[0], 'Play again', 30),
               Button(screen, [screen.get_width() / 2, screen.get_height() // 2 - 50], '',
                      f'You scored {variables[1]:.2f}% on {directory[directory.find("/") + 1:directory.find(".")]}',
                      30),
               Button(screen, [screen.get_width() / 2, screen.get_height() // 2 + 110], 'level selection',
                      'Return to level selection', 30)]
    outro_g.add(outro_l)
    if high_scores[str(variables[0])] < variables[1]:
        high_scores[str(variables[0])] = variables[1] * 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file_writer()
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'level selection'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(outro_g.sprites())):
                        s = outro_g.sprites()[i]
                        pos = pygame.mouse.get_pos()
                        if s.rect.collidepoint(pos[0], pos[1]) and (
                                isinstance(outro_l[i].mode_c, int) or outro_l[i].mode_c):
                            return outro_l[i].mode_c
        screen.fill('light gray')
        outro_g.draw(screen)
        outro_g.update()
        pygame.display.update()


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


def draw_rect_alpha(surface, color, rect):
    if pygame.Rect(rect).bottom > 0:
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)
        return True


def note_extractor(which_level, slow_down) -> list[list[str, float, float, bool]]:
    """
    :return: list[list[note, length of note, bottomdist from bottom, if needs to be held], ...]
    """
    notes = []
    multi = 1 * slow_down
    hold_threshold = 1
    with open(f'MachineNotes/{which_level}.txt') as f:
        times = f.read().count('\n')
        f.seek(0)
        for _ in range(times):
            machine_notes: list[str] = f.readline().replace('[', '').replace(']', '') \
                .replace("'", '').replace('\n', '').split(', ')
            dist_from_bottom = 0
            for line in machine_notes:  # a#-#
                if line[0] == '|':
                    multi = eval(line[1:line.find('-',2)]) / slow_down
                elif line[0].isalpha():
                    leng = eval(line[1:line.find("-",2)]) * multi
                    notes.append([line[0], leng * 60, dist_from_bottom, leng > hold_threshold])
                    leng = eval(line[line.find("-") + 1:]) * multi
                    dist_from_bottom += leng * 60
                else:  # line[0] is space
                    leng = eval(line[1:line.find("-",2)]) * multi
                    dist_from_bottom += leng * 60
    notes.sort(key=lambda notes: notes[2] + notes[1])
    # print(notes)
    return notes


def make_text(x, y, what, t_size=30, color='blue'):
    if y > 0:
        text = pygame.font.Font('Fonts/Roboto-Light.ttf', t_size).render(str(what), True, color)
        screen.blit(text, text.get_rect(center=(x, y)))


if __name__ == "__main__":
    main()
