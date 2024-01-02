"""
`1234567890-=
qwertyuiop[]\
asdfghjkl;'
zxcvbnm,./
K_F[1-15]
K_SPACE
K_BACKSPACE
K_CAPSLOCK
K_TAB
K_LSHIFT
K_RSHIFT
K_LCTRL
K_RCTRL
K_UP
K_DOWN
K_LEFT
K_RIGHT
K_LALT
K_RALT
"""
import mido
import csv
from os import listdir


MIN_HOLD_NOTE_LEN: float = 1.0  # min length of a held note (sec)
MIN_TAP_NOTE_SIZE: int = 10  # pixels
DEFAULT_VELOCITY: float = 60.0  # velocity used if all notes in a song are held
MIN_VELOCITY: float = 150
MAX_VELOCITY: float = 500
# any notes that have a duration less than this value is removed
MIN_NOTE_LEN_MS: float = 10

MAX_KEYS_IN_NORMAL: int = 48
INPUT_DIR = 'Assets/Midi/'
OUTPUT_DIR = 'Assets/MachineNotes/'

instruction = list[int, float, float, int]  # note name, note duration, note distance from playing, is held


def process_file(file_name: str) -> None:
    """
    Process a .mid or .midi file to a set of note instructions listed in a .csv with the file's name
    """
    print(f"Processing {file_name}:")
    mid = mido.MidiFile(INPUT_DIR + file_name)

    VELOCITY = get_velocity(mid)

    notes: list[instruction] = get_note_instructions(mid)
    compressed_notes = linear_compression(notes)
    overlap = get_overlap(compressed_notes)
    cutting_points = sorted(get_cutting_points(overlap))
    notes = combine_buckets(compressed_notes, cutting_points)
    print(len(cutting_points))

    write_to_csv(file_name, VELOCITY, notes)


def combine_buckets(compressed_notes, cutting_points):
    max_bucket_id = len(cutting_points)
    new_notes = []
    bucket_status_end = {i: 0 for i in range(max_bucket_id + 1)}
    deleted_notes = 0
    deleted_note_buckets = {i: 0 for i in range(max_bucket_id + 1)}
    num_notes_in_bucket = {i: 0 for i in range(max_bucket_id + 1)}
    for note, *rest in compressed_notes:
        bucket_id = max_bucket_id + note / 100
        for i, cutting_point in enumerate(cutting_points):
            if note < cutting_point:
                bucket_id = i + note / 100  # cuttedBucket.compressedBucket
                break
        if bucket_status_end[int(bucket_id)] > rest[1]:  # if the bucket not empty, then can't add note
            deleted_notes += 1
            deleted_note_buckets[int(bucket_id)] += 1
            continue
        num_notes_in_bucket[int(bucket_id)] += 1
        bucket_status_end[int(bucket_id)] = rest[1] + rest[0]
        
        new_notes.append([bucket_id, *rest])
    
    print("# of deleted notes (overlap):", deleted_notes)
    if deleted_notes != 0:
        print(deleted_note_buckets)
    print(num_notes_in_bucket)

    return new_notes


def get_note_instructions(mid):
    curTime = 0
    notesStatus = {i : 0 for i in range(88)}
    notes = []
    removed = 0
    for msg in mid:
        curTime += msg.time
        if msg.type != "note_on" and msg.type != "note_off":
            continue
        if msg.type == "note_on" and msg.velocity != 0:
            notesStatus[msg.note] = curTime
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
            time_till_note = notesStatus[msg.note]

            note_len_sec = curTime - notesStatus[msg.note]

            if note_len_sec < MIN_NOTE_LEN_MS / 1000:
                removed += 1
                continue

            notes.append([
                msg.note,
                note_len_sec,
                time_till_note
                ])
    print("# of removed notes (too short):", removed)
    return notes


def write_to_csv(file_name, VELOCITY, notes):
    with open(OUTPUT_DIR + file_name.replace('.mid', '.csv'), 'w', newline='') as csvfile:
        csvfile.write(str(VELOCITY) + '\n')
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(notes)

def linear_compression(notes):
    # Compress notes into list of minimum buckets so each note is distinct
    linear_key = {}
    all_notes = set()
    for note, *_ in notes:
        all_notes.add(note)
    for i, note in enumerate(sorted(all_notes)):
        linear_key[note] = i
    new_notes = []
    for note, *rest in notes:
        new_notes.append([linear_key[note], *rest])
    return new_notes


def get_overlap(notes) -> dict[tuple[int, int], int]:
    """
    Get the dictionary of pair of notes that are overlapping with one another (the pair is always ascending)
    """
    overlaps = []
    note_on = {i[0]: -1 for i in notes}
    for i in notes:
        for j, loc in note_on.items():  # Edge case: i should not be on while j is on
            if i[2] >= loc - 0.001:  # if i is played after j is finished, subtract 0.01 to ignore edge
                continue
            a = min(i[0],j)
            b = max(i[0],j)
            overlaps.append((a,b))
        note_on[i[0]] = i[1]+i[2]
    overlap_matrix: dict[tuple[int, int], int] = {}
    for overlap in overlaps:
        if overlap in overlap_matrix:
            overlap_matrix[overlap] += 1
        else:
            overlap_matrix[overlap] = 1
    return overlap_matrix


def get_cutting_points(overlap_matrix):
    def cut_matrix(matrix, cut):
        newMatrix = matrix.copy()
        for pair, n in matrix.items():
            if cut > pair[0] and cut <= pair[1]:
                newMatrix.pop(pair)
        return newMatrix

    cuts = []
    for _ in range(MAX_KEYS_IN_NORMAL - 1):
        cutLocations = {i:0 for i in range(128)}
        for pair, n in overlap_matrix.items():
            for cutLocation in range(pair[0]+1, pair[1]+1):
                cutLocations[cutLocation]+=n
        
        cutLocationsList = sorted(cutLocations.items(), key=lambda i: i[1], reverse=True)
        cut = cutLocationsList[0][0]
        if cut == 0:
            return cuts
        cuts.append(cut) #return most advantageous cut
        overlap_matrix = cut_matrix(overlap_matrix, cut)
    return cuts


def get_velocity(mid):
    curTime = 0
    notesStatus = {i : 0 for i in range(88)}

    min_note_len: float = 1_000 # secs
    for msg in mid:
        curTime += msg.time
        if msg.type == "note_on" and msg.velocity != 0:
            notesStatus[msg.note] = curTime
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
            min_note_len = min(min_note_len, curTime - notesStatus[msg.note])
            notesStatus[msg.note] = curTime
        if min_note_len < MIN_NOTE_LEN_MS / 1000:
            min_note_len = MIN_NOTE_LEN_MS / 1000
    if min_note_len < MIN_HOLD_NOTE_LEN:
        VELOCITY = max(min(MIN_TAP_NOTE_SIZE / min_note_len, MAX_VELOCITY), MIN_VELOCITY)
    else:  # all notes are to be held
        VELOCITY = DEFAULT_VELOCITY
    return VELOCITY


for file_name in listdir(INPUT_DIR):
    if file_name.endswith(".mid") or file_name.endswith(".midi"):
        process_file(file_name)
