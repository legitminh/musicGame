import csv
from constants import SONG_PATHS
from gui.note import Note, NoteGroup


def midi_note_extractor(which_level: int, slowdown: float, extreme: bool, velocity: float) -> tuple[float, NoteGroup]:
    notes = NoteGroup()
    multi = 1 / slowdown
    with open(SONG_PATHS[which_level].replace("Musics", "Assets/MachineNotes").replace(".wav", ".csv")) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        _velocity = float(csv_file.readline().strip())
        for bucket_id, note_len, dist_to_bottom in reader:
            notes.add(
                Note(
                    float(bucket_id) if extreme else int(float(bucket_id)), 
                    float(note_len) * multi * velocity, 
                    float(dist_to_bottom) * multi * velocity
                )
            )
    notes.rename_buckets()
    return _velocity, notes
