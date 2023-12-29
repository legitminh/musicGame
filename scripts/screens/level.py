"""
This file handels displaying the level screen.

TODO: incorporate more note numbers
TODO: responsive system
    - Change column color/note color
"""


import pygame
from interfaces import *
from utility.readMachineNotes import midi_note_extractor
from UI import make_text, draw_rect_alpha
from .screen import Screen
from constants import *
from typing import Any


BUCKET_NUMBER_INDEX = 0
DURATION_INDEX = 1
DIST_FROM_BOTOM_INDEX = 2
LINE_LEVEL = 0.8


class Level(Screen):
    """
    This class handels displaying the level and player interaction.
    """
    slowdown: float
    volume: float
    extreme = False
    # bucket_key_order = [pygame.K_f, pygame.K_j]
    # the order for which the buckets are created, the first bucket will have an input key of "`", the second bucket will have an input key of "1", and so on.
    bucket_display_order = [
        pygame.K_BACKQUOTE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS,
        pygame.K_TAB, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET,
        pygame.K_CAPSLOCK, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE,
        pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT,
        # pygame.K_
        # pygame.K_NUMLOCK, pygame.K_KP_DIVIDE, 
    ]
    # the names of the buckets
    bucket_name_order = [
        *"`1234567890-",
        "Tb",*"qwertyuiop[",
        "Cp",*"asdfghjkl;'",
        "Ls",*"zxcvbnm,./","Rs"
    ]
    dt = 0

    correct_hits = 0
    total_hits = 0
    last_time = pygame.time.get_ticks()
    first_hit = True
    

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs: Any) -> None:
        """
        Creates a level object.

        Args:
            screen (pygame.Surface): The surface that the level object will draw itself on.
            clock (pygame.time.Clock): The clock which will be used to set the maximum fps.
            **kwargs (Any): Any other arguments, will ignore all values other than `volume`, `song_id`, `extreme`, and `slowdown`.
                volume (float): The volume the songs will be played at.
                song_id (int): The id of the song that will be played. 
                extreme (bool): If the level will be the "extreme" varient.
                slowdown (int | float): The amount the song will be slow downed 
                    (will run the pre-slow-downed version of the song located in the "ProcessedMusics" directory)
        
        Returns: 
            None
        
        Raises:
            ValueError: If `volume`, `song_id`, `extreme`, or `slowdown` are not included in `kwargs`.
        """
        tmp = kwargs.copy()
        arguments = {'volume': float, 'song_id': int, 'extreme': bool, 'slowdown': int | float}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        
        kwargs = tmp
        for arg, arg_type in arguments.items():
            if arg not in kwargs or not isinstance(kwargs[arg], arg_type):
                raise ValueError("Key word argument not included or is of an unacceptable type.")
        
        super().__init__(screen, clock, **kwargs)
        
        self._note_init()
        pygame.mixer.music.set_volume(self.volume)
    
    def loop(self) -> Redirect:
        """
        The main game loop.

        Returns:
            Redirect: A screen redirect.
        
        Raises:
            ExitException: If the user exits out of the screen.
        """
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
            if self.first_hit: self.dt = 0
            self.last_time = pygame.time.get_ticks()
            
            ret_val = self._update_notes()
            if ret_val is not None:
                return ret_val
            
            self._draw()
        
    def _note_init(self) -> None:
        """
        Initializes the notes, velocity, and buckets by reading from machine notes.

        Returns:
            None
        """
        bucket = int | float
        duration = float
        dist_from_bottom = float
        self.notes: list[list[bucket, duration, dist_from_bottom]]
        self.velocity, self.notes = midi_note_extractor(self.song_id, self.slowdown, self.extreme)
        # get bucket number
        buckets = set(note[0] for note in self.notes)
        self.bucket_number = len(buckets)
        if self.extreme:
            bucket_conv = {e: i for i, e in enumerate(sorted(buckets))}
            self.notes = [[bucket_conv[bucket_id], *rest] for bucket_id, *rest in self.notes]
        self.bucket_size = self.screen.get_width() / self.bucket_number

    def _all_note_cycle(self) -> None:  # note GFX
        """
        Moves the notes down by `velocity` pixles every second.

        Returns:
            None
        """
        for note in self.notes:
            draw_rect_alpha(
                self.screen, NOTE_COLOR, (  # every bucket is in one row
                note[BUCKET_NUMBER_INDEX] * self.bucket_size, 
                self.screen.get_height() * LINE_LEVEL - note[DIST_FROM_BOTOM_INDEX] - note[DURATION_INDEX],
                self.bucket_size, note[DURATION_INDEX],
                )
            )
            note[DIST_FROM_BOTOM_INDEX] -= self.dt * self.velocity
    
    def _draw_key_names(self) -> None:
        """
        Draws the names of each bucket.

        Returns:
            None
        """
        for bucket in range(self.bucket_number):
            make_text(self.screen, self.bucket_size * (bucket + 0.5), self.screen.get_height() * .9, self.bucket_name_order[bucket])
    
    def _update_notes(self) -> Redirect | None:
        """
        Checks if the the song has ended and removes notes if said note falls below the screen.

        Returns:
            Redirect: If the song has ended.
            None: If the song has not ended.
        """
        if len(self.notes) == 0:  # check if finished song
            pygame.mixer.music.stop()
            try:
                return Redirect(
                    ScreenID.outro, 
                    song_id=self.song_id, 
                    score=self.correct_hits / self.total_hits * 100,
                    slowdown=self.slowdown,
                    extreme=self.extreme
                    )
            except ZeroDivisionError:
                return Redirect(ScreenID.levelOptions, song_id=self.song_id)
        for note in self.notes:
            if note[DURATION_INDEX] + note[DIST_FROM_BOTOM_INDEX] >= -self.screen.get_height() * (1 - LINE_LEVEL): # top of note above the hititng bar
                break
            self.total_hits += 1
            self.notes.pop(0)
        
    def _draw(self) -> None:
        """
        Draws all elements onto the screen.

        Returns:
            None
        """
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
    
    def _key_up(self, event) -> None: 
        """
        Checks if a key up event coincides with the end of a note.

        Returns:
            None
        """
        bucket_id = self._convert_key_to_bucket_id(event.key)
        if bucket_id is None: return
        for i, note in enumerate(self.notes):
            if note[BUCKET_NUMBER_INDEX] != bucket_id:
                continue
            if not (note[DIST_FROM_BOTOM_INDEX] <= 0 <= note[DIST_FROM_BOTOM_INDEX] + note[DURATION_INDEX]):  # if not in colliding range
                break
            if abs(note[DIST_FROM_BOTOM_INDEX] + note[DURATION_INDEX]) <= LENIENCY * self.velocity:
                self.notes.pop(i)
                self.total_hits += 1
                self.correct_hits += 1
                break

    def _down_hit(self, bucket_id) -> None: 
        """
        Checks if a key down event coincides with the start of a note.

        Returns:
            None
        """
        for note in self.notes:
            if note[BUCKET_NUMBER_INDEX] != bucket_id: continue
            if abs(note[DIST_FROM_BOTOM_INDEX]) <= LENIENCY * self.velocity:
                self.total_hits += 1
                self.correct_hits += 1
                break
    
    def _convert_key_to_bucket_id(self, key) -> int | None:
        """
        Converts a key to it's corresponding bucket id (an int).

        Returns:
            int: A bucket id.
            None: If the key does not correspond to a bucket.
        """
        if key in self.bucket_display_order:
            return self.bucket_display_order.index(key)
    
    def _key_down(self, event) -> None:
        """
        Starts the song if the first key was hit and checks if a key pressed corresponds to a bucket other wise.

        Returns:
            None
        """
        #start the song
        if self.first_hit:
            if self.slowdown < 1:
                pygame.mixer.music.load(SONG_PATHS[self.song_id].replace("Musics/","ProcessedMusics/").replace(".wav",f'{int(self.slowdown * 100)}.wav'))
            else:
                pygame.mixer.music.load(SONG_PATHS[self.song_id])
            pygame.mixer.music.play()
            self.last_time = pygame.time.get_ticks()
            self.first_hit = False
        bucket_id = self._convert_key_to_bucket_id( event.key )
        if bucket_id is None: return
        self._down_hit(bucket_id)
