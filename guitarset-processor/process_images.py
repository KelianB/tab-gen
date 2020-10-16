import os
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

AUDIO_SAMPLE_RATE = 44100 # Hz
plt.ioff()

def get_cqt(audio_path, segment_index, segment_length):
    start = segment_index * segment_length
    
    # Pour diminuer le bruit
    #def cqt_lim(CQT):
    #    new_CQT = np.copy(CQT)
    #    new_CQT[new_CQT < -60] = -120
    #    return new_CQT

    # Perform the Constant-Q Transform
    data, sr = librosa.load(audio_path, sr=AUDIO_SAMPLE_RATE, mono=True, offset=start, duration=segment_length)
    CQT = librosa.cqt(data, sr=AUDIO_SAMPLE_RATE, hop_length=512, fmin=None, n_bins=96, bins_per_octave=12)
    CQT_mag = librosa.magphase(CQT)[0]**4
    CQTdB = librosa.core.amplitude_to_db(CQT_mag, ref = np.amax)
    #new_CQT = cqt_lim(CQTdB)
    return CQTdB
    
def plot_cqt(audio_path, segment_index, segment_length):
    cqt = get_cqt(audio_path, segment_index, segment_length)
    
    fig, ax = plt.subplots()
    img = librosa.display.specshow(cqt, sr=AUDIO_SAMPLE_RATE, x_axis='time', y_axis='cqt_note', ax=ax)
    ax.set_title('Constant-Q power spectrum')
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.show()

def save_image(audio_path, output_path, segment_index, segment_length):
    cqt = get_cqt(audio_path, segment_index, segment_length)
    
    plt.clf()
    fig, ax = plt.subplots()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    img = librosa.display.specshow(cqt, sr=AUDIO_SAMPLE_RATE, ax=ax, cmap="gray_r")
    plt.savefig(output_path)

def create_segmented_inputs(jam, segment_length, raw_dir, processed_dir):
    audio_file = os.path.join(raw_dir, jam.file_metadata.title + "_mic.wav")
    num_segments = math.ceil(jam.file_metadata.duration / segment_length)

    for i in range(num_segments):
        filename = jam.file_metadata.title + "_" + str(i) + ".png"
        print(filename)
        output_file = os.path.join(processed_dir, filename)
        save_image(audio_file, output_file, i, segment_length)
    
if __name__ == "__main__":
    # Testing

    # Load audio and define paths
    AUDIO_ROOT = "./raw/audio/"
    audio_files = os.listdir(AUDIO_ROOT)
    audio_path = os.path.join(AUDIO_ROOT, "00_BN1-129-Eb_comp_mic.wav")
    plot_cqt(audio_path, 0, 0.2)


