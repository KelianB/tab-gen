import matplotlib
import librosa
import numpy as np
import soundfile as sf


example_audio = librosa.util.example_audio_file()
x, sr = librosa.load(example_audio, duration=5)
print('shape of x ==> ' + str(x.shape))
y, sr = librosa.load(example_audio, duration=5)
print('shape of y ==> ' + str(y.shape))
z = np.append(x,y)
print('shape of x+y = z ==> ' + str(z.shape))
sf.write('joined_file.wav', z, sr)

z_loaded, sr = librosa.load('joined_file.wav')
print('shape of z loaded ==> ' + str(z_loaded.shape))
