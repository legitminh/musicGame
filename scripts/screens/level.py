import pygame
from interfaces import *


class Level:

    def extreme_level(screen, which, slowdown) -> tuple[str, float] | str:
        if isinstance(which, str) and 'e' in which:
            which = int(which.replace('e', ''))
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
        note_numbers = {} #option and their colum number(x postion)
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
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return (mode_choice, [which])
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
                                # if isinstance(e, TypeError):
                                #     print(e, i, holds)
                                pass
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
                    return (outro, [str(which) + 'e', correct_hits / total_hits * 100, slowdown])
                except ZeroDivisionError:
                    return (mode_choice, [which])
            
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
                (0, 0, 255, 100), (255, 0, 255, 100)]
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
                    return
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
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #ESC to exit song
                        pygame.mixer.music.stop()
                        return (mode_choice, [which])
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
                                pass
                                # if isinstance(e, TypeError):
                                #     print(e, i, holds)
            if len(notes) == 0:  # check if finished song
                pygame.mixer.music.stop()
                try:
                    return (outro, [which, correct_hits / total_hits * 100, slowdown])
                except ZeroDivisionError:
                    return (mode_choice, [which])
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
