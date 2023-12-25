import mido
import csv
from os import listdir
import math

MIN_HOLD_NOTE_LEN: float = 1.0  # min length of a held note (sec)
MIN_TAP_NOTE_SIZE: int = 10  # pixles
DEFAULT_VELOCITY: float = 60.0  # velocity used if all notes in a song are held
MIN_VELOCITY: float = 75
MAX_VELOCITY: float = 250
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

INPUT_DIR = 'Assets/Midi/'
OUTPUT_DIR = 'Assets/MachineNotes/'
BUCKET_NUM = 10

instruction = list[int, float, float, int]  # note name, note duration, note distance from playing, is held


def process_file(file_name: str) -> None:
    """
    Process a .mid or .midi file to a set of note instructions listed in a .csv with the file's name
    """
    mid = mido.MidiFile(INPUT_DIR + file_name)

    VELOCITY = get_velocity(mid)

    notes: list[instruction] = get_note_instructions(mid, VELOCITY)
    
    notes: list[instruction] = buketfy(notes)

    write_to_csv(file_name, VELOCITY, notes)


def get_note_instructions(mid, velocity):
    curTime = 0
    notesStatus = {i : 0 for i in range(88)}
    notes = []
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

            notes.append([
                msg.note,
                round(note_len_px, 3),
                round(dist_till_note, 3),
                int(note_len_sec > MIN_HOLD_NOTE_LEN),
                ])
    return notes


def write_to_csv(file_name, VELOCITY, notes):
    with open(OUTPUT_DIR + file_name.replace('.mid', '.csv'), 'w', newline='') as csvfile:
        csvfile.write(str(VELOCITY) + '\n')
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(notes)


def buketfy(notes) -> list[instruction]:
    """
    Return list of notes but now the lable is as bucket id's instead of note id's
    Bucket size: the number of notes that belong to a single bucket; notes must 
        be adjacent
    - Adjusts bucket sizes so that the standard deviation of the number of notes 
        belonging to a bucket is minimized
    - Removes notes that cannot be placed in a bucket
    - Minimizes the number of notes that are removed
    - Trys setting most of the notes in the middle
    """
    highest_note = max( [i[0] for i in notes] )
    lowest_note = min( [i[0] for i in notes] )
    bucket_size = math.ceil((highest_note - lowest_note+1) / BUCKET_NUM) 
    new_notes = []
    bucket_status_start = {i:0 for i in range(BUCKET_NUM)}
    bucket_status_end = {i:0 for i in range(BUCKET_NUM)}
    deleted_notes = 0
    
    for note in notes:
        bucket_id = (note[0] - lowest_note) // bucket_size
        if bucket_status_end[bucket_id] > note[2]:  # if the bucket not empty, then can't add note
            deleted_notes += 1
            continue
        bucket_status_start[bucket_id] =  note[2]
        bucket_status_end[bucket_id] = bucket_status_start[bucket_id] + note[1]
        new_notes.append([bucket_id, *note[1:]])
    print(deleted_notes)
    return new_notes


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
    if min_note_len < MIN_HOLD_NOTE_LEN:
        VELOCITY = max(min(MIN_TAP_NOTE_SIZE / min_note_len, MAX_VELOCITY), MIN_VELOCITY)
    else:  # all notes are to be held
        VELOCITY = DEFAULT_VELOCITY
    return VELOCITY


for file_name in listdir(INPUT_DIR):
    if file_name.endswith(".midi"):
        file_name.replace(".midi", ".mid")
    if file_name.endswith(".mid"):
        process_file(file_name)
