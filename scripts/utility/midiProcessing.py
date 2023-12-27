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
import math
from itertools import combinations
from functools import lru_cache

MIN_HOLD_NOTE_LEN: float = 1.0  # min length of a held note (sec)
MIN_TAP_NOTE_SIZE: int = 10  # pixels
DEFAULT_VELOCITY: float = 60.0  # velocity used if all notes in a song are held
MIN_VELOCITY: float = 75
MAX_VELOCITY: float = 250
# any notes that have a duration less than this value is removed
MIN_NOTE_LEN_MS: float = 40
CONV_NOTE_NUM: dict[int, str] = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B',
}

MAX_KEYS_IN_NORMAL: int = 48
INPUT_DIR = 'Assets/Midi/'
OUTPUT_DIR = 'Assets/MachineNotes/'
# BUCKET_NUM = 10

instruction = list[int, float, float, int]  # note name, note duration, note distance from playing, is held


def process_file(file_name: str) -> None:
    """
    Process a .mid or .midi file to a set of note instructions listed in a .csv with the file's name
    """
    print(f"Processing {file_name}>>>")
    mid = mido.MidiFile(INPUT_DIR + file_name)

    VELOCITY = get_velocity(mid)

    notes: list[instruction] = get_note_instructions(mid, VELOCITY)
    compressed_notes = linear_compression(notes)
    cutting_points = sorted(get_cutting_points(get_overlap(compressed_notes)))
    notes = combine_buckets(compressed_notes, cutting_points)
    # if cutting_points[0] == cutting_points[1] == 0:
    #     print('Static')
    #     highest_note = max( [i[0] for i in notes] )
    #     lowest_note = min( [i[0] for i in notes] )
    #     bucket_size = math.ceil((highest_note - lowest_note+1) / BUCKET_NUM) 
    #     cutting_points = [lowest_note + bucket_size * i for i in range(1, BUCKET_NUM)]
    # condensed_notes = buketfy(notes, cutting_points) #these notes are condensed to where each key doesn't overlap

    # write_to_csv(file_name, VELOCITY, notes)


def combine_buckets(compressed_notes, cutting_points):

    max_bucket_id = len(cutting_points)
    new_notes = []
    bucket_status_end = {i: 0 for i in range(max_bucket_id)}
    deleted_notes = 0
    deleted_note_buckets = {i: 0 for i in range(max_bucket_id)}
    num_notes_in_bucket = {i: 0 for i in range(max_bucket_id)}
    for note, *rest in compressed_notes:
        bucket_id = max_bucket_id + note / 100 - 1
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
        


def get_note_instructions(mid, velocity):
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
            dist_till_note = time_till_note * velocity

            note_len_sec = curTime - notesStatus[msg.note]
            note_len_px = velocity * note_len_sec

            if note_len_sec < MIN_NOTE_LEN_MS / 1000:
                removed += 1
                continue

            notes.append([
                msg.note,
                round(note_len_px, 3),
                round(dist_till_note, 3),
                int(note_len_sec > MIN_HOLD_NOTE_LEN),
                ])
    # print("# of removed notes (too short):", removed)
    return notes


def write_to_csv(file_name, VELOCITY, notes):
    return
    with open(OUTPUT_DIR + file_name.replace('.mid', '.csv'), 'w', newline='') as csvfile:
        csvfile.write(str(VELOCITY) + '\n')
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(notes)

def buketfy(notes, bucket) -> list[instruction]:
    """
    Return list of notes but now the lable is as bucket id's instead of note id's
    Bucket size: the number of notes that belong to a single bucket; notes must 
        be adjacent
    - Removes notes that cannot be placed in a bucket
    - Minimizes the number of notes that are removed
    - Adjusts bucket sizes so that the standard deviation of the number of notes 
        belonging to a bucket is minimized
    - Trys setting most of the notes in the middle
    """
    new_notes = []
    bucket_status_end = {i: 0 for i in range(BUCKET_NUM)}
    deleted_notes = 0
    deleted_note_buckets = {i: 0 for i in range(BUCKET_NUM)}
    num_notes_in_bucket = {i: 0 for i in range(BUCKET_NUM)}
    
    for note in notes:
        bucket_id = BUCKET_NUM - 1
        for i, cutting_point in enumerate(bucket):
            if note[0] < cutting_point:
                bucket_id = i
                break

        if bucket_status_end[bucket_id] > note[2]:  # if the bucket not empty, then can't add note
            deleted_notes += 1
            deleted_note_buckets[bucket_id] += 1
            continue
        num_notes_in_bucket[bucket_id] += 1   



        bucket_status_end[bucket_id] = note[2] + note[1]
        new_notes.append([bucket_id, *note[1:]])
    print("# of deleted notes (overlap):", deleted_notes)
    # if deleted_notes != 0:
    #     print(deleted_note_buckets)
    # print(num_notes_in_bucket)
    return new_notes

def linear_compression(notes):
    # Compress notes into list of minimum buckets so each note is distinct
    lowest = 0
    linear_key = {}
    new_notes = []
    for note, *rest in notes:
        if note in linear_key:
            new_notes.append([linear_key[note], *rest])
        else:
            linear_key[note] = lowest
            new_notes.append([linear_key[note], *rest])
            lowest += 1
    return new_notes


def seperate_by_note(notes) -> dict[int, list[float, float]]:
    note_vals: dict[int, list[float, float]] = {}
    for note in notes:
        if note[0] in note_vals:
            note_vals[note[0]].append(note[1], note[2])
        else:
            note_vals[note[0]] = [[note[1], note[2]]]
    return dict(sorted(note_vals, key=lambda x: x[0]))


def get_overlap(notes) -> dict[tuple[int, int], int]:
    """
    Get the list of two notes that are overlapping with one another
    """
    overlaps = []
    note_on = {i[0]: -1 for i in notes}
    for i in notes:
        for j, loc in note_on.items():  # Edge case: i should not be on while j is on
            if i[2] < loc:  # if i is played before j is finished
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
    """
    Get all cutting point required to prevent overlap
    """
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

# def get_cutting_points_1(notes, cuts):
#     """
#     A cutting point is the first point in each bucket
#     """
#     def cut_matrix(matrix, cut):
#         newMatrix = matrix.copy()
#         for pair, n in matrix.items():
#             if cut > pair[0] and cut <= pair[1]:
#                 newMatrix.pop(pair)
#         return newMatrix

#     cuts = []
#     for _ in range(max_buckets - 1):
#         cutLocations = {i:0 for i in range(128)}
#         for pair, n in overlap_matrix.items():
#             for cutLocation in range(pair[0]+1, pair[1]+1):
#                 cutLocations[cutLocation]+=n
        
#         cutLocationsList = sorted(cutLocations.items(), key=lambda i: i[1], reverse=True)
#         cut = cutLocationsList[0][0]
#         cuts.append(cut) #return most advantageous cut
#         overlap_matrix = cut_matrix(overlap_matrix, cut)
#     return cuts

def get_velocity(mid):
    curTime = 0
    notesStatus = {i : 0 for i in range(88)}

    # min note length (sec) -> speed
    # speed -> note length (px) for all notes
    min_note_len: float = 1_000 # secs
    for msg in mid:
        curTime += msg.time
        if msg.type == "note_on" and msg.velocity != 0:
            notesStatus[msg.note] = curTime
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):  # two ways people notate note_off
            min_note_len = min(min_note_len, curTime - notesStatus[msg.note])
            notesStatus[msg.note] = curTime
        if min_note_len < MIN_NOTE_LEN_MS / 1000:
            min_note_len = MIN_NOTE_LEN_MS / 1000
    if min_note_len < MIN_HOLD_NOTE_LEN:
        VELOCITY = max(MIN_TAP_NOTE_SIZE / min_note_len, MIN_VELOCITY)
    else:  # all notes are to be held
        VELOCITY = DEFAULT_VELOCITY
    return VELOCITY


for file_name in listdir(INPUT_DIR):
    if file_name.endswith(".midi"):
        file_name.replace(".midi", ".mid")
    if file_name.endswith(".mid"):
        process_file(file_name)
