
Inputs = "Musics"
Outputs = "ProcessedMusics"
from os import listdir

print(listdir(Inputs))
import librosa
import soundfile as sf
for file in listdir(Inputs):
    if file.endswith(".wav") or file.endswith(".mp3"):
        signal, sr = librosa.load(Inputs + '/' + file)
        for slow in range(3):
            changed_signal = librosa.effects.time_stretch(signal, rate=(slow+1)*.25)
            sf.write(f'{Outputs}/{file.replace(".",f"{(slow+1)*25}.")}', changed_signal, sr)