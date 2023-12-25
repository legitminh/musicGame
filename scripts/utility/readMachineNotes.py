#transform machine notes into a list of note commands
import csv
from constants import SONG_PATHS

def midi_note_extractor(which_level: int, slowdown: float):
    notes = []
    multi = 1 / slowdown
    with open(SONG_PATHS[which_level].replace("Musics", "Assets/MachineNotes").replace(".wav", ".csv")) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        velocity = float(csvfile.readline().strip())
        for note, note_len, dist_to_bottom, hold in reader:
            notes.append([note, float(note_len) * multi, float(dist_to_bottom) * multi, bool(int(hold))])
    return velocity, notes


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
    return notes
