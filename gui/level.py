"""
This file handels displaying the level screen.
"""


import pygame
from .interfaces import *
from utility.readMachineNotes import midi_note_extractor
from .UI import make_text, draw_rect_alpha
from .screen import Screen
from constants import *
from typing import Any
from gui.note import NoteGroup

BUCKET_NUMBER_INDEX = 0
DURATION_INDEX = 1
DIST_FROM_BOTTOM_INDEX = 2


class Level(Screen):
    """
    This class handles displaying the level and player interaction.
    """
    slowdown: float
    volume: float
    velocity: float
    song_id: int
    bucket_settings: dict[int, tuple[int, str]]
    extreme = False
    background_surface: pygame.surface.Surface

    key_to_bucket: dict[int, int]
    
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
            **kwargs (Any): Any other arguments, will ignore all values other than `volume`, `velocity`, `song_id`, `extreme`, `slowdown`, and `bucket_settings`.
                volume (float): The volume the song will be played at.
                velocity (float): The velocity the song will be played at.
                song_id (int): The id of the song that will be played. 
                extreme (bool): If the level will be the "extreme" variant.
                slowdown (int | float): The amount the song will be slow downed 
                    (will run the pre-slow-downed version of the song located in the "ProcessedMusics" directory).
                bucket_settings (dict[int, str]): The key id and key name associated with each bucket id.
        
        Returns: 
            None
        
        Raises:
            ValueError: If `volume`, `velocity`, `song_id`, `extreme`, `slowdown`, or `bucket_settings` are not included in `kwargs`.
        """
        tmp = kwargs.copy()
        arguments = {'volume': float, 'velocity': float, 'song_id': int, 'extreme': bool, 'slowdown': int | float, 'bucket_settings': dict}
        for kwarg in kwargs:
            if kwarg not in arguments:
                tmp.pop(kwarg)
        
        kwargs = tmp
        for arg, arg_type in arguments.items():
            if arg not in kwargs or not isinstance(kwargs[arg], arg_type):
                raise ValueError("Key word argument not included or is of an unacceptable type.")
        
        super().__init__(screen, clock, **kwargs)
        
        self._note_init()
        self._render_background()
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
                if event.type == pygame.VIDEORESIZE:
                    self._render_background()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        return Redirect(ScreenID.levelOptions, song_id=self.song_id)
                    self._key_down(event)
                elif event.type == pygame.KEYUP:
                    self._key_up(event)
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
        self.notes: NoteGroup
        self.velocity = 100 + 1400 * self.velocity
        _, self.notes = midi_note_extractor(self.song_id, self.slowdown, self.extreme, self.velocity)

        self.key_to_bucket = {a: i for i, [a, _] in enumerate(self.bucket_settings.values())}
    
    def _render_background(self) -> None:
        """
        Renders the background of the level and stores it as a pygame surface to be displayed later.
        This function is called at the start of a level and every time the screen size changes.

        Returns:
            None
        """
        self.background_surface = pygame.Surface(self.screen.get_size())
        for i in range(self.notes.num_buckets):
            bucket_width = self.screen.get_width() / self.notes.num_buckets
            ALT_PERIOD = 2 if self.notes.num_buckets < 12 else 4
            draw_rect_alpha(self.background_surface, (ALT_COLOR if (i // ALT_PERIOD) % 2 else BACKGROUND_COLOR), [i*bucket_width , 0, (i+1)*bucket_width, self.screen.get_height()], 0, border_radius=0)
        
        alternate = True
        for bucket in range(self.notes.num_buckets):
            text = pygame.font.Font('Assets/Fonts/Roboto-Light.ttf', 24).render(str(self.bucket_settings[bucket][1]), True, "blue")
            pos = self.screen.get_width() / self.notes.num_buckets * (bucket + 0.5), self.screen.get_height() * .9 + (-8 if alternate else 8)
            self.background_surface.blit(text, text.get_rect(center=pos))
            alternate = not alternate

    def _all_note_cycle(self) -> None:
        """
        Moves the notes down by `velocity` pixels every second.

        Returns:
            None
        """
        self.notes.draw(self.screen)
        self.notes.update(self.dt * self.velocity)
    
    def _update_notes(self) -> Redirect | None:
        """
        Checks if the the song has ended and removes notes if said note falls below the screen.

        Returns:
            Redirect: If the song has ended.
            None: If the song has not ended.
        """
        if len(self.notes) == 0:
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
            if note.note_duration + note.dist_from_bottom >= -self.screen.get_height() * (1 - LINE_LEVEL): # top of note above the hitting bar
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
        self.screen.blit(self.background_surface, (0, 0))
            
        self._all_note_cycle()
        
        pygame.draw.line(self.screen, LINE_COLOR, (0, line_px_level), (self.screen.get_width(), line_px_level))
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
        self.total_hits += 1
        bucket_id = self.key_to_bucket.get(event.key)
        if bucket_id is None: return
        for note in self.notes.get_bucket(bucket_id):
            note.unpressed()
            if 0 < note.dist_from_bottom:
                break
            if 0 < note.dist_from_bottom + note.note_duration <= LENIENCY * self.velocity:
                self.notes.remove(note)
                self.correct_hits += 1
                break

    def _down_hit(self, bucket_id) -> None: 
        """
        Checks if a key down event coincides with the start of a note.

        Returns:
            None
        """
        print(f"down hit at {bucket_id}")
        for note in self.notes.get_bucket(bucket_id):
            if 0 > note.dist_from_bottom >= -LENIENCY * self.velocity and not note.key_down_awarded:
                self.correct_hits += 1
                note.key_down_awarded = True
                note.pressed()
                break
    
    def _key_down(self, event) -> None:
        """
        Starts the song if the first key was hit and checks if a key pressed corresponds to a bucket other wise.

        Returns:
            None
        """
        if self.first_hit:
            if self.slowdown < 1:
                pygame.mixer.music.load(SONG_PATHS[self.song_id].replace("Musics/","ProcessedMusics/").replace(".wav",f'{int(self.slowdown * 100)}.wav'))
            else:
                pygame.mixer.music.load(SONG_PATHS[self.song_id])
            pygame.mixer.music.play()
            self.last_time = pygame.time.get_ticks()
            self.first_hit = False
            return
        self.total_hits += 1
        
        bucket_id = self.key_to_bucket.get(event.key)
        if bucket_id is None: return
        self._down_hit(bucket_id)
