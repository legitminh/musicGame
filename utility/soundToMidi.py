import librosa
from sound_to_midi.monophonic import wave_to_midi
from os import listdir
from tqdm import tqdm

INPUT_DIR = 'Assets/Audio/'
OUTPUT_DIR = 'Assets/Midi2/'


def process_file(file_name):
    file_out = OUTPUT_DIR + file_name.replace(file_name[-4:], ".mid")
    print(f"\nLoading \"{file_name}\"...")
    y, sr = librosa.load(INPUT_DIR + file_name, sr=None)
    print(f"Processing \"{file_name}\"...")
    midi = wave_to_midi(y, srate=sr)
    print(f"Writing processed file...")
    with open (file_out, 'wb') as f:
        midi.writeFile(f)


for file_name in tqdm(listdir(INPUT_DIR)):
    if file_name.replace(file_name[-4:], ".mid") in listdir(OUTPUT_DIR):
        print("fileAlreadyLoaded")
        continue
    if file_name.endswith(".mp3") or file_name.endswith(".wav"):
        process_file(file_name)
