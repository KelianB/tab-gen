import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

AUDIO_ROOT = "./raw/audio/"

#files = filter(lambda file: file[-5:] == ".jams", os.listdir(ANNOTATIONS_ROOT))
#files = list(files)[0:n]
start = 0
SEGMENT_LENGTH = 0.2

# Load audio and define paths
audio_file = os.listdir(AUDIO_ROOT)
audio_path = os.path.join(AUDIO_ROOT, audio_file[0])

# Pour diminuer le bruit
def cqt_lim(CQT):
    new_CQT = np.copy(CQT)
    new_CQT[new_CQT < -60] = -120
    return new_CQT

# Perform the Constant-Q Transform
data, sr = librosa.load(audio_path, sr = None, mono = True, offset = start, duration = SEGMENT_LENGTH)
CQT = librosa.cqt(data, sr = 44100, hop_length = 512, fmin = None, n_bins = 96, bins_per_octave = 12)
CQT_mag = librosa.magphase(CQT)[0]**4
CQTdB = librosa.core.amplitude_to_db(CQT_mag, ref = np.amax)
#new_CQT = cqt_lim(CQTdB)
fig, ax = plt.subplots()
img = librosa.display.specshow((CQTdB), sr=sr, x_axis='time', y_axis='cqt_note', ax=ax)
ax.set_title('Constant-Q power spectrum')
fig.colorbar(img, ax=ax, format="%+2.0f dB")
plt.show()