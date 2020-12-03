import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from matplotlib.figure import Figure
import torch
import cv2
from model_class import GuitarSetModel
from playback import create_audio
import pathlib
pathlib.PosixPath = pathlib.WindowsPath

MODEL_PATH = "./model_best.pth"
AUDIO_SAMPLE_RATE = 44100 # Hz
SEGMENT_LENGTH = 0.2 # s

# Turn matplotlib's interactive mode off
plt.ioff()

def load_model():
    model = GuitarSetModel()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu"), )["state_dict"])
    return model


def infer(model, img):
    output = model(img[np.newaxis])
    predictions = torch.argmax(output, dim=2)
    return predictions[0].tolist()


def cqt_image_generator(audio_data, max_duration):
    """
        Generates a Constant-Q transform for each audio segment in a given audio time series.
        
        Parameters:
            audio_data (np.ndarray) : audio time series for an entire audio file.
        
        Returns: List<np.ndarray>
            a list of CQT data
    """
    duration = librosa.get_duration(audio_data, AUDIO_SAMPLE_RATE)
    num_segments = math.floor(min(max_duration, duration) / SEGMENT_LENGTH)
    # print("duration =", duration, "| segments =", num_segments, "| shape =", audio_data.shape)

    samples_per_segment = math.floor(AUDIO_SAMPLE_RATE * SEGMENT_LENGTH)
    for i in range(num_segments):
        segment_data = audio_data[i * samples_per_segment : (i + 1) * samples_per_segment]
        cqt = compute_cqt(segment_data)
        img = render_cqt_image(cqt)
        print("{0:.1f}".format(100 * i / num_segments) + "%", end="\r")
        yield img


def compute_cqt(data):
    """
        Compute the Constant-Q transform for a single segment of a given audio file.
        
        Parameters:
            data (np.ndarray) : audio time series for one segment of audio.
        
        Returns: np.ndarray
            the spectrogram associated with the processed segments, in dB, as a numpy array.
    """
    
    # Perform the Constant-Q Transform
    CQT = librosa.cqt(data, sr=AUDIO_SAMPLE_RATE, hop_length=512, fmin=None, n_bins=96, bins_per_octave=12)
    CQT_mag = librosa.magphase(CQT)[0]**4
    
    # Convert to dB
    CQTdB = librosa.core.amplitude_to_db(CQT_mag, ref = np.amax)

    return CQTdB


def render_cqt_image(cqt):
    """
        Plot a Constant-Q transform.
        
        Parameters:
            cqt (np.ndarray): a spectrogram (see compute_cqt).
    """

    plt.close("all")
    fig, ax = plt.subplots()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    librosa.display.specshow(cqt, sr=AUDIO_SAMPLE_RATE, ax=ax, cmap="gray_r")
    
    # Get image data from the plot
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # Convert to an opencv image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Resize & convert
    img = cv2.resize(img, (160, 120), interpolation=cv2.INTER_CUBIC)
    img = torch.from_numpy(np.array([img])).float()

    return img


# Testing
if __name__ == "__main__":
    #AUDIO_FILE = "./test_inputs/input_00_BN1-129-Eb_comp_mic.wav"
    AUDIO_FILE = "./test_inputs/input_mario.wav"
    MAX_DURATION = 30
    
    print("Loading model...", end="\r")
    model = load_model() 
    print("Model loaded.\t\t")
    
    print("Loading input audio...", end="\r")
    data, sr = librosa.load(AUDIO_FILE, sr=AUDIO_SAMPLE_RATE, mono=True)
    print("Input audio loaded.\t\t\t")
    
    """
    for i, img in enumerate(cqt_image_generator(data, MAX_DURATION)):
        #plt.close("all")
        #plt.figure(figsize=(3, 4))
        #imgplot = plt.imshow(img, cmap="gray")
        #plt.show()
        cv2.imshow("img - " + str(i), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    """

    print("Computing chords...", end="\r")
    chords = [infer(model, img) for img in cqt_image_generator(data, MAX_DURATION)]
    print("Computed chords.\t\t\t")

    create_audio(chords, playback=True, save_to_file="output.wav")