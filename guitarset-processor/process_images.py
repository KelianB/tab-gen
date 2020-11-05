import os
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

AUDIO_SAMPLE_RATE = 44100 # Hz

# Whether or not to replace the pre-existing images
OVERWRITE_IMAGES = False 

# Turn matplotlib's interactive mode off
plt.ioff()


def compute_cqt(audio_path, segment_index, segment_length):
    """
        Compute the Constant-Q transform for a single segment of a given audio file.
        
        Parameters:
            audio_path     (string): the path to an audio file.
            segment_index  (int)   : the index of the audio segment to process.
            segment_length (float) : the segmentation interval.
        
        Returns: np.ndarray
            the spectrogram associated with the processed segments, in dB, as a numpy array.
    """
    start = segment_index * segment_length
    
    # Load audio data
    data, sr = librosa.load(audio_path, sr=AUDIO_SAMPLE_RATE, mono=True, offset=start, duration=segment_length)
    
    # Perform the Constant-Q Transform
    CQT = librosa.cqt(data, sr=AUDIO_SAMPLE_RATE, hop_length=512, fmin=None, n_bins=96, bins_per_octave=12)
    CQT_mag = librosa.magphase(CQT)[0]**4
    
    # Convert to dB
    CQTdB = librosa.core.amplitude_to_db(CQT_mag, ref = np.amax)

    # Reduce noise
    #def cqt_lim(CQT):
    #    new_CQT = np.copy(CQT)
    #    new_CQT[new_CQT < -60] = -120
    #    return new_CQT
    #new_CQT = cqt_lim(CQTdB)
    return CQTdB


def plot_cqt(cqt):
    """
        Plot a Constant-Q transform.
        
        Parameters:
            cqt (np.ndarray): a spectrogram (see compute_cqt).
    """

    fig, ax = plt.subplots()
    img = librosa.display.specshow(cqt, sr=AUDIO_SAMPLE_RATE, x_axis='time', y_axis='cqt_note', ax=ax)
    ax.set_title("Constant-Q power spectrum")
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.show()


def save_image(cqt, output_path):
    """
        Save a spectrogram to a given output file.
        
        Parameters:
            cqt          (np.ndarray): a spectrogram (see compute_cqt).
            output_path      (string): the path to save the image.
    """

    plt.close("all")
    fig, ax = plt.subplots()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    img = librosa.display.specshow(cqt, sr=AUDIO_SAMPLE_RATE, ax=ax, cmap="gray_r")
    plt.savefig(output_path)


def create_segmented_inputs(jam, segment_length, raw_dir, processed_dir):
    """
        Create and save the spectrogram for each segment of a dataset entry.
        
        Parameters:
            jam                    : a parsed annotation file (.jams).
            segment_length  (float): the segmentation interval.
            raw_dir        (string): the path to the directory where the raw data is stored.
            processed_dir  (string): the path to the directory where the images will be saved.
    """

    audio_file = os.path.join(raw_dir, jam.file_metadata.title + "_mic.wav")
    num_segments = math.floor(jam.file_metadata.duration / segment_length)
    num_segments -= 1 # Remove the last segment, which is likely to have incomplete audio data

    # Iterate over segments
    for i in range(num_segments):
        filename = jam.file_metadata.title + "_" + str(i) + ".png"
        output_file = os.path.join(processed_dir, filename)

        # Compute and save the spectrogram only if needed
        if OVERWRITE_IMAGES or not os.path.isfile(output_file):
            cqt = compute_cqt(audio_file, i, segment_length)
            save_image(cqt, output_file)


# Testing
if __name__ == "__main__":
    # Load audio and define paths
    AUDIO_ROOT = "./raw/audio/"
    audio_files = os.listdir(AUDIO_ROOT)
    audio_path = os.path.join(AUDIO_ROOT, "00_BN1-129-Eb_comp_mic.wav")
    cqt = compute_cqt(audio_path, 0, 0.2)
    plot_cqt(cqt)


