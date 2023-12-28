import csv
from constants import SONG_PATHS


def midi_note_extractor(which_level: int, slowdown: float, extreme: bool):
    notes = []
    multi = 1 / slowdown
    with open(SONG_PATHS[which_level].replace("Musics", "Assets/MachineNotes").replace(".wav", ".csv")) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        velocity = float(csvfile.readline().strip())
        for note, note_len, dist_to_bottom in reader:
            notes.append([float(note) if extreme else int(float(note)), float(note_len) * multi, float(dist_to_bottom) * multi])
    return velocity, notes
