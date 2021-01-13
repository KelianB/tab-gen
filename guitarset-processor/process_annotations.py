import os
import jams
import math
import numpy as np
from collections import namedtuple

# Initialize the matrix used to convert midi values to guitar chords
frets = np.zeros((6, 18), dtype=np.int32)
for q in range(0, 6):
    qs = [40, 45, 50, 55, 59, 64]
    for f in range(0, 18):
        frets[q, f] = qs[q] + f


def get_annotation_files(n, annotations_dir):
    """
        Get n parsed annotation files (.jams) from a given directory.
        
        Parameters:
            n                (int): the number of files fo parse.
            annotations_dir  (int): the directory to pull from.
        
        Returns: list(parsed jams)
            a list of parsed jams files.
    """

    print("0.0%", end="\r")

    # Get the files in the directory and filter for .jams
    files = list(filter(lambda file: file[-5:] == ".jams", os.listdir(annotations_dir)))
    
    # Keep the first n files and map to their complete location
    files = list(map(lambda file: os.path.join(annotations_dir, file), files[0:n]))
    
    loaded = [] 
    # Load the files using the jams library
    N = len(files)
    for i,path in enumerate(files):
        loaded.append(jams.load(path))
        print("{0:.1f}".format(100 * i / N) + "%\t", end="\r")
    print("\t" * 5, end="\r")

    return loaded


def compute_overlap_frequency(jam, segment_length):
    """
        Compute the percentage of overlapping segments for a given annotation file with a given segment length.
        Two segments overlap if a note spans over both of them.
        
        Parameters:
            jam                   : a parsed .jams file (see get_annotation_files).
            segment_length (float): the segmentation interval.
        
        Returns: float
            the frequency (in the [0,1] range) of overlapping segments.
    """

    strings = jam.search(namespace="note_midi")

    total_segments = 0
    overlapping_segments = 0

    # For each guitar string
    for string_notes in strings:
        segment_notes = []
        # For each note
        for note in string_notes:
            start_segment_idx = math.floor(note.time / segment_length)
            end_segment_idx   = math.floor((note.time + note.duration) / segment_length)
            
            # Ensure the segment_notes list is large enough
            while end_segment_idx > len(segment_notes) - 1:
                segment_notes.append(0)

            # Increment the note counter for each segment this note overlaps
            for j in range(start_segment_idx, end_segment_idx + 1):
                segment_notes[j] += 1

        total_segments += len(segment_notes)
        overlapping_segments += len(list(filter(lambda n: n > 1, segment_notes)))
    
    return overlapping_segments / total_segments    


def visualize_overlap_frequencies(parsed_jams):
    """
        Visualize the average percentage of overlapping segments for the given annotation files, for a range of segment lengths.
        
        Parameters:
            parsed_jams: a list of parsed .jams files (see get_annotation_files).
    """

    import matplotlib.pyplot as plt

    # Function that computes the average overlap frequency for a given segment_length
    f = lambda seg_len: sum(compute_overlap_frequency(jam, seg_len) for jam in parsed_jams) / len(parsed_jams)

    # Set x values (segment lengths) and calculate corresponding averages 
    x = np.linspace(0.01, 0.2, num=20)
    y = np.vectorize(f)(x)

    # Plot the results
    plt.title("Note overlap (averaged over %d recordings)" % len(parsed_jams))
    plt.xlabel("Segment length (seconds)")
    plt.ylabel("% segments with more than 1 note")
    plt.plot(x, y)
    plt.show()


def get_segmented_outputs(jam, segment_length):
    """
        Compute the guitar chords for all segments of a given annotation file with a given segment length.
        
        Parameters:
            jam                   : a parsed .jams file (see get_annotation_files).
            segment_length (float): the segmentation interval.
        
        Returns: list(list(int))
            a list of values for each fixed-duration segment.
            each segment is associated with 6 values corresponding to the note that is played on each string (0 means none).
    """

    strings = jam.search(namespace="note_midi")
    num_segments = math.ceil(jam.file_metadata.duration / segment_length)
    segments = [[0, 0, 0, 0, 0, 0] for _ in range(num_segments)]

    MIDINote = namedtuple("SegmentedNote", ["time", "duration", "value"])

    num_overlaps = 0
     
    # For each guitar string
    for i, string_notes in enumerate(strings):
        # First, sort the notes in 0.2s segments.
        # For example: [[{time: 0.04s, duration, value}, {time: 0.12s, duration, value}], [{time: 0.04s, duration, value}], ...]
        # The same note can appear multiple times, in the case where it intersects with several segments.
        segment_notes = [[] for _ in range(num_segments)]
        for note in string_notes:
            start_segment_idx = math.floor(note.time / segment_length)
            end_segment_idx   = math.floor((note.time + note.duration) / segment_length)

            for j in range(start_segment_idx, end_segment_idx + 1):
                segment_notes[j].append(MIDINote(time=note.time % segment_length, duration=note.duration, value=note.value))

        # num_overlaps += len(list(filter(lambda notes: len(notes) > 1, segment_notes)))

        # We then need to go from n notes per segment to 0 or 1 note per segment
        # Strategy: always keep the last note
        for j, notes in enumerate(segment_notes):
            if len(notes) > 0:
                segments[j][i] = round(notes[-1].value)
        
    # print("Overlapping segments:", num_overlaps, "/", (6*num_segments), "(" + ("%.2f" % (100 * num_overlaps / (6*num_segments))) + "%)")

    # Remove the last segment, which is likely to have incomplete audio data
    segments = segments[:-2] 

    # Finally, the notes (midi values) are converted to guitar chords 
    return [to_guitar_chords(segment) for segment in segments]


def to_guitar_chords(midi_values):
    """
        Compute the guitar chords associated with midi values.
        
        Parameters:
            midi_values (list(float)): a list of 6 MIDI values, one for each guitar string.
        
        Returns: list(int)
            a list of frets to press on each string of a guitar (0 means no note is played, 1 means open string)
    """

    tab = np.zeros((6, 19), dtype=np.int32)
    for s, midi in enumerate(midi_values):
        match = (frets[s] == int(midi)) * 1
        # Add a column at the beginning to indicate if no note is being played
        string = np.hstack(([0 if np.any(match) else 1], match))
        tab[s,:] = string

    # Convert to indices to save space in storage
    indices = np.where(tab == 1)[1]

    return indices

