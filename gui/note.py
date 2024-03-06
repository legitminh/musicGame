import pygame
from .UI import draw_rect_alpha
from constants import *
from collections.abc import Iterable


class Note:
    """
    A class to represent a note.
    """
    __is_held = False
    key_down_awarded = False

    def __init__(self, bucket_number: int | float, note_duration: float, dist_from_bottom: float) -> None:
        """
        Creates a note.
        
        Args:
            bucket_number (int | float): The bucket the note belongs to.
            note_duration (float): The duration of the note in pixels.
            dist_from_bottom (float): The distance the note is from the line where the player can hit it.
        """
        self.bucket_number = bucket_number
        self.note_duration = note_duration
        self.dist_from_bottom = dist_from_bottom
    
    def update(self, dt: float) -> None:
        """
        Updates `dist_from_bottom` by `dt`.

        Args:
            dt (float): The distance traveled by the note.
        """
        self.dist_from_bottom -= dt
        if self.dist_from_bottom + self.note_duration <= 0:
            self.unpressed()

    def draw(self, screen: pygame.Surface, bucket_size) -> None:
        """
        Draws the note on the screen.

        Args:
            screen (pygame.Surface): The surface that the note will draw itself on.
        """
        if self.__is_held and self.dist_from_bottom + self.note_duration > 0:
            draw_rect_alpha(
                screen, FILL_COMPLETE_COLOR if 0 < self.dist_from_bottom + self.note_duration <= 0.5 * 150 else FILL_COLOR, (  # every bucket is in one row
                self.bucket_number * bucket_size, 
                screen.get_height() * LINE_LEVEL,
                bucket_size, abs(self.dist_from_bottom),
                ), width=0,
            )
        draw_rect_alpha(
            screen, NOTE_COLOR, (  # every bucket is in one row
            self.bucket_number * bucket_size, 
            screen.get_height() * LINE_LEVEL - self.dist_from_bottom - self.note_duration,
            bucket_size, self.note_duration,
            )
        )
    
    def pressed(self):
        self.__is_held = True

    def unpressed(self):
        self.__is_held = False

class NoteGroup:
    """
    A class that holds all notes part of a song.
    """

    __num_buckets = None

    def __init__(self) -> None:
        """
        Creates a group of notes.
        """
        self.notes: list[Note] = []
        self.buckets: dict[int, list[Note]] = {}

    def add(self, note: Note) -> None:
        """
        Adds a note to `self.buckets` and `self.all_notes`.

        Args:
            note (Note): The note to be added to the group of notes.
        """
        self.notes.append(note)
        if note.bucket_number in self.buckets:
            self.buckets[note.bucket_number].append(note)
        else:
            self.buckets[note.bucket_number] = [note]
    
    def rename_buckets(self):
        """
        Reassigns a bucket number to each note so that the notes all have integer bucket numbers.

        Examples:
            >>> notes = NoteGroup()
            ... (add notes to `notes`)
            >>> [note.bucket_number for note in notes]
            [3.2, 1.3, 2.1, 1.3, 2.0]
            >>> notes.rename_buckets()
            >>> [note.bucket_number for note in notes]
            [4, 1, 3, 1, 2]
        """
        buckets = set(note.bucket_number for note in self.notes)
        bucket_conv = {e: i for i, e in enumerate(sorted(buckets))}
        self.buckets: dict[int, list[Note]] = {}
        for note in self.notes:
            note.bucket_number = bucket_conv[note.bucket_number]
            if note.bucket_number in self.buckets:
                self.buckets[note.bucket_number].append(note)
            else:
                self.buckets[note.bucket_number] = [note]
        
    
    
    def update(self, dt: float) -> None:
        """
        Updates all notes by `dt` using the note's `update` method.

        Args:
            dt (float): The distance traveled by all of the notes.
        """
        [note.update(dt) for note in self.notes]
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all notes using the note's `draw` method.

        Args:
            screen (pygame.Surface): The surface that the notes will be drawn on.
        """
        [note.draw(screen, screen.get_width() / self.num_buckets) for note in self.notes]
    
    def get_bucket(self, bucket_number: int) -> list[Note]:
        """
        Gets all notes in a certain bucket.

        Args:
            bucket_number (int): The bucket number.
        
        Returns:
            list[Note]: A list of all notes with a bucket number of `bucket_number`.
        """
        if bucket_number in self.buckets:
            return self.buckets[bucket_number]
        return []
    
    def pop(self, index: int = -1) -> Note:
        """
        Remove and return item at `index`, default last.

        Args:
            index (int): The index of the value to be removed.

        Returns:
            Note: The note at `index`.

        Raises:
            IndexError: If no item exists at `index`
        """
        tmp = self.notes.pop(index)
        self.buckets[tmp.bucket_number].remove(tmp)
        return tmp

    def remove(self, note: Note) -> None:
        """
        Remove the first `note` from `notes`.

        Args:
            note (Note): The note to be removed.
        
        Raises:
            ValueError: If `note` is not in `notes`.
        """
        note.unpressed()
        self.notes.remove(note)
        self.buckets[note.bucket_number].remove(note)

    @property
    def num_buckets(self) -> int:
        """
        Gets the number of buckets that have at least one note in them.

        Returns:
            int: The number of buckets with at least one note in it.
        """
        if self.__num_buckets is None:
            self.__num_buckets = len(set(note.bucket_number for note in self.notes))
        return self.__num_buckets

    def __iter__(self) -> Iterable[Note]:
        """
        Allows a for loop to operate on a `NoteGroup` object.

        Returns:
            Iterable[Note]: an iterator of `self.all_notes`.
        """
        return iter(self.notes.copy())
    
    def __len__(self) -> int:
        """
        Returns the length of notes in the group of notes.

        Returns:
            int: The number of notes in the group of notes.
        """
        return len(self.notes)
