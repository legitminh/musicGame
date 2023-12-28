import pygame
from interfaces import *
from utility.readMachineNotes import midi_note_extractor
from random import choice
from UI import make_text, draw_rect_alpha
from .screen import Screen
from constants import *


BUCKET_NUMBER_INDEX = 0
DURATION_INDEX = 1
DIST_FROM_BOTOM_INDEX = 2
LINE_LEVEL = 0.8


class Level(Screen):
    slowdown: float
    volume: float
    extreme = False
    ""
    # bucket_key_order = [pygame.K_f, pygame.K_j]
    bucket_display_order = [
        pygame.K_BACKQUOTE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS,
        pygame.K_TAB, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET,
        pygame.K_CAPSLOCK, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE,
        pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT
    ]
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
                elif event.type == pygame.VIDEORESIZE:
                    self.bucket_size = self.screen.get_width() / self.bucket_number
            self.dt = (pygame.time.get_ticks() - self.last_time) / 1000
            if self.first: self.dt = 0
            self.last_time = pygame.time.get_ticks()
            
            ret_val = self._update_notes()
            if ret_val is not None:
                return ret_val
            
            self._draw()
        
    def _note_init(self):
        bucket = int | float
        duration = float
        dist_from_bottom = float
        self.notes: list[list[bucket, duration, dist_from_bottom]]
        self.velocity, self.notes = midi_note_extractor(self.song_id, self.slowdown, self.extreme)
        #get bucket number
        buckets = set()
        for note in self.notes:
            buckets.add(note[0])
        self.bucket_number = len(buckets)
        self.bucket_size = self.screen.get_width() / self.bucket_number

    def _all_note_cycle(self):  # note GFX
        for note in self.notes:
            draw_rect_alpha(
                self.screen, NOTE_COLOR, (  # every bucket is in one row
                note[BUCKET_NUMBER_INDEX] * self.bucket_size, 
                self.screen.get_height() * LINE_LEVEL - note[DIST_FROM_BOTOM_INDEX] - note[DURATION_INDEX],
                self.bucket_size, note[DURATION_INDEX],
                )
            )
            note[DIST_FROM_BOTOM_INDEX] -= self.dt * self.velocity
    
    def _draw_key_names(self):
        for bucket in range(self.bucket_number):
            # change the name of each bucket from it's number to something more descriptive        vvvvvv
            make_text(self.screen, self.bucket_size * (bucket + 0.5), self.screen.get_height() * .9, bucket)
    
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
            if note[DURATION_INDEX] + note[DIST_FROM_BOTOM_INDEX] >= 0: # top of note above the hititng bar
                break
            self.total_hits += 1
            self.notes.pop(0)
        
    def _draw(self):
        line_px_level = int(self.screen.get_height() * LINE_LEVEL)
        self.screen.fill('gray')
        pygame.draw.line(self.screen, 'black', (0, line_px_level), (self.screen.get_width(), line_px_level))
            
        self._all_note_cycle()
        self._draw_key_names()
        try:
            make_text(self.screen, self.screen.get_width() / 2, 20, round(self.correct_hits / self.total_hits * 100, 2))
        except ZeroDivisionError:
            make_text(self.screen, self.screen.get_width() / 2, 20, 0)
        pygame.display.update()
        self.clock.tick(FRAME_RATE)
    
    def _key_up(self, event): 
        bucket_id = self._convert_key_to_bucket_id(event.key)
        if bucket_id is None: return
        for note in self.notes:
            if note[BUCKET_NUMBER_INDEX] != bucket_id:
                continue
            if not (note[DIST_FROM_BOTOM_INDEX] <= 0 <= note[DIST_FROM_BOTOM_INDEX] + note[DURATION_INDEX]):  # if not in colliding range
                break
            if abs(note[DIST_FROM_BOTOM_INDEX] + note[DURATION_INDEX]) <= LENIENCY * self.velocity:
                self.total_hits += 1
                self.correct_hits += 1
                break

    def _down_hit(self, bucket_id): 
        for note in self.notes:
            if note[BUCKET_NUMBER_INDEX] != bucket_id: continue
            if abs(note[DIST_FROM_BOTOM_INDEX]) <= LENIENCY * self.velocity:
                self.total_hits += 1
                self.correct_hits += 1
                break
    
    def _convert_key_to_bucket_id(self, key):
        if key in self.bucket_display_order:
            return self.bucket_display_order.index(key)
        return None
    
    def _key_down(self, event):
        #start the song
        if self.first:
            if self.slowdown < 1:
                pygame.mixer.music.load(SONG_PATHS[self.song_id].replace("Musics/","ProcessedMusics/").replace(".wav",f'{int(self.slowdown * 100)}.wav'))
            else:
                pygame.mixer.music.load(SONG_PATHS[self.song_id])
            pygame.mixer.music.play()
            self.last_time = pygame.time.get_ticks()
            self.first = False
        bucket_id = self._convert_key_to_bucket_id( event.key )
        if bucket_id is None: return
        self._down_hit(bucket_id)
