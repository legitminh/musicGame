import pygame
from interfaces import *
from utility.readMachineNotes import *
from random import choice
from UI import make_text, draw_rect_alpha
from .screen import Screen
from constants import *


class Level(Screen):
    slowdown: float
    volume: float
    extreme = False
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
    colors = [(255, 0, 0, 100), (255, 165, 0, 100), (255, 255, 0, 100), (0, 255, 0, 100), (0, 255, 255, 100),
            (0, 0, 255, 100), (255, 0, 255, 100)]
    dt = 0

    correct_hits = 0
    total_hits = 0
    last_time = pygame.time.get_ticks()
    first = True

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs):
        super().__init__(screen, clock, **kwargs)
        
        if isinstance(self.song_id, str):
            if 'e' in self.song_id:
                self.song_id = int(self.song_id.replace('e', ''))
                self.extreme = True
            else:
                self.song_id = int(self.song_id)
            
        self._note_init()
        pygame.mixer.music.set_volume(self.volume)
    
    def loop(self) -> ScreenID:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #ESC to exit song
                        pygame.mixer.music.stop()
                        return Redirect(ScreenID.levelOptions, song_id=(str(self.song_id) + 'e') if self.extreme else self.song_id)
                    self._key_down(event)
                elif event.type == pygame.KEYUP:
                    self._key_up(event)
            self.dt = (pygame.time.get_ticks() - self.last_time) / 1000
            if self.first: self.dt = 0
            self.last_time = pygame.time.get_ticks()
            
            ret_val = self._update_notes()
            if ret_val is not None:
                return ret_val
            
            self._draw()
        
    def _note_init(self):
        _notes = {'0': 'q', '1': 'w', '2': 'e', '3': 'r', '4': 't', '5': 'y', '6': 'u', '7': 'i', '8': 'o', '9': 'p'}
        if self.extreme:
            self.note_numbers = {}
            self.note_rep = {}
            self.holds: dict[str, None | float] = {}
            for i, options in enumerate(self.note_change.values()):
                for rank, option in enumerate(options):
                    self.holds[option] = None
                    self.note_numbers[option] = i
                    self.note_rep[option] = rank
        else:
            self.note_numbers = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9}
            self.holds: dict[str, None | float] = {
                'q': None, 'w': None, 'e': None, 'r': None, 't': None, 'y': None, 'u': None, 'i': None, 'o': None, 'p': None
                }
        self.velocity, self.notes = midi_note_extractor(self.song_id, self.slowdown)
        for i, note in enumerate(self.notes):
            self.notes[i][0] = _notes[note[0]]

        if self.extreme:
            for i, note in enumerate(self.notes):
                note[0] = choice(self.note_change[note[0]])
    
    def _all_note_cycle(self):  # note GFX
        current_color = 0
        notes_copy = self.notes[:]
        notes_copy.reverse()
        for note in notes_copy:  # check list representing note
            if note[2] <= 0 <= note[2] + note[1]:
                color = (0, 255, 0, 255)  # green-clickable
            else:
                color = self.colors[current_color]
                current_color += 1
                if current_color == len(self.colors):
                    current_color = 0
            if self.holds[note[0]] == 0 and note[2] <= 0 <= note[2] + note[1] and note[3]:
                color = (255, 0, 0, 255)
            draw_rect_alpha(self.screen, color, (
                self.note_numbers[note[0]] * self.screen.get_width() / 10, self.screen.get_height() * .8 - note[2] - note[1],
                self.screen.get_width() / 10, note[1]))
            note[2] -= self.dt * self.velocity  # decrease time>>note fall down.
    
    def _draw_key_rank(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        for note in self.notes:
            if self.note_rep[note[0]] != 0:
                if height * .8 - note[2] - note[1]/2 - 8 < 0:
                    break
                self.screen.blit(pygame.image.load(f"Assets/Images/Extreme/{self.note_rep[note[0]]}.png"),
                (self.note_numbers[note[0]] * width / 10+ width / 20-8,
                height * .8 - note[2] - note[1]/2 - 8))
    
    def _draw_key_names(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        lowest: list[int] = []
        for note in self.notes:
            if self.note_numbers[note[0]] in lowest:
                continue
            if len(lowest) == 10:
                return
            lowest.append(self.note_numbers[note[0]])
            make_text(self.screen, self.note_numbers[note[0]] * width / 10 + width / 20, height * .9, note[0])
    
    def _update_notes(self):
        if len(self.notes) == 0:  # check if finished song
            pygame.mixer.music.stop()
            song_id = (str(self.song_id) + 'e') if self.extreme else self.song_id
            try:
                return Redirect(
                    ScreenID.outro, 
                    song_id=song_id, 
                    score=self.correct_hits / self.total_hits * 100,
                    slowdown=self.slowdown,
                    )
            except ZeroDivisionError:
                return Redirect(ScreenID.levelOptions, song_id=song_id)
        for note in self.notes:
            if note[2] + note[1] >= 0: # don't remove
                break
            self.total_hits += 1
            self.holds[note[0]] = None
            self.notes.pop(0)
        for a in self.holds.keys():
            if type(self.holds[a]) is float:  # is being held
                if self.holds[a] > 0:
                    self.holds[a] -= self.dt * 60
                else:
                    self.holds[a] = 0

    def _draw(self):
        line_level = int(self.screen.get_height() * .8)
        self.screen.fill('gray')
        pygame.draw.line(self.screen, 'black', (0, line_level), (self.screen.get_width(), line_level))
            
        self._all_note_cycle()
        if self.extreme:
            self._draw_key_names()
            self._draw_key_rank()
        else:
            for i in ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']:
                make_text(self.screen, (self.note_numbers[i] + .5) * self.screen.get_width() / 10, self.screen.get_height() * .9, i.upper())
        try:
            make_text(self.screen, self.screen.get_width() / 2, 20, int(self.correct_hits / self.total_hits * 100))
        except ZeroDivisionError:
            make_text(self.screen, self.screen.get_width() / 2, 20, 0)
        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def _key_up(self, event):
        for i in self.notes:
            if i[2] <= 0 <= i[2] + i[1] and i[3]:  # if in colliding range
                try:  #
                    if event.key in range(32, 127) and self.holds[i[0]] <= 0 and i[3]:
                        self.total_hits += 1
                        self.correct_hits += 1
                        self.holds[i[0]] = None
                        self.notes.remove(i)
                except Exception as e:
                    pass

    def _key_down(self, event):
        if self.first:
            if self.slowdown < .99:
                pygame.mixer.music.load(SONG_PATHS[self.song_id].replace("Musics/","ProcessedMusics/").replace(".wav",f'{int(self.slowdown * 100)}.wav'))
            else:
                pygame.mixer.music.load(SONG_PATHS[self.song_id])
            pygame.mixer.music.play()
            self.last_time = pygame.time.get_ticks()
            self.first = False
        clicked = False
        keys = pygame.key.get_pressed()
        for i in self.notes:  # i = note
            if i[2] > 0 or 0 > i[2] + i[1]:  # if key not in range
                break
            if not keys[ord(i[0])]: continue
            clicked = True
            if i[3]:
                self.holds[i[0]] = i[1] * .5
            else:
                self.notes.remove(i)
                self.total_hits += 1
                self.correct_hits += 1
        if not clicked and event.key in range(97, 123):
            self.total_hits += 1
