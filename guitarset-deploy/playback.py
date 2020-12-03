
import simpleaudio as sa
import soundfile as sf
import time
import numpy as np

# Utility functions to play chords using sine waves.

OUTPUT_SAMPLE_RATE = 44100 # Hz

def prepare_audio(frequencies, dur):
    # Get timesteps for each sample, T is note duration in seconds
    t = np.linspace(0, dur, int(dur * OUTPUT_SAMPLE_RATE), False)

    if len(frequencies) == 0:
            return (0 * t).astype(np.int16)

    # Generate sine wave notes
    notes =  [np.sin(f * t * 2 * np.pi) for f in frequencies]

    # Sum the notes
    audio = np.sum(notes, axis=0)
    
    # Normalize to 16-bit range and convert to 16-bit
    if len(frequencies) > 0:
        audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    return audio


def play_audio(audio_buffer):
    return sa.play_buffer(audio_buffer, 1, 2, OUTPUT_SAMPLE_RATE)


def compute_frequency(string, fret):
    a3_freq = 220
    half_tone = 2 ** (1 / 12)

    higher_from_a3_by = 5 * (string - 2) + (fret - 1)
    if string > 4:
        higher_from_a3_by += 1
    return a3_freq * half_tone ** higher_from_a3_by


def compute_frequencies(frets):
    frequencies = []
    for i in range(6):
        if frets[i] != 0:
            frequencies.append(compute_frequency(i + 1, frets[i]))
    return frequencies


def create_audio(chords, playback=False, save_to_file=None):    
    print("Preparing audio data...", end="\r")

    # Convert the chords to frequencies
    frequencies = [compute_frequencies(frets) for frets in chords]
    
    # Compute and concatenate the audio data
    audio_data = np.hstack([prepare_audio(freqs, 0.2) for freqs in frequencies])
    
    print("Audio data ready.\t\t\t")

    if save_to_file != None:
        sf.write(save_to_file, audio_data, OUTPUT_SAMPLE_RATE)  
    
    if playback:
        input("Press enter to start playing")
        play_audio(audio_data).wait_done()


