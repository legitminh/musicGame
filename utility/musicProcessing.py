from os import listdir
import librosa
import soundfile as sf
import tqdm

Inputs = "Musics"
Outputs = "ProcessedMusics"

print(listdir(Inputs))
for file in tqdm.tqdm(listdir(Inputs)):
    if not (file.endswith(".wav") or file.endswith(".mp3")):
        continue
    signal, sr = librosa.load(Inputs + '/' + file)
    for slow in range(3):
        changed_signal = librosa.effects.time_stretch(signal, rate=(slow+1)*.25)
        sf.write(f'{Outputs}/{file.replace(".",f"{(slow+1)*25}.")}', changed_signal, sr)
