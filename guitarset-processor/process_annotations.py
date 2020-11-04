import os
import jams
import math
import numpy as np
from collections import namedtuple

def get_annotation_files(n, annotations_dir):
    files = filter(lambda file: file[-5:] == ".jams", os.listdir(annotations_dir))
    files = list(files)[0:n]
    return list(map(lambda file: jams.load(os.path.join(annotations_dir, file)), files))

def compute_overlap_frequency(jam, segment_length):
    strings = jam.search(namespace="note_midi")

    total_segments = 0
    overlapping_segments = 0

    for string_notes in strings:
        segment_notes = []
        for note in string_notes:
            start_segment_idx = math.floor(note.time / segment_length)
            end_segment_idx   = math.floor((note.time + note.duration) / segment_length)
            
            while end_segment_idx > len(segment_notes) - 1:
                segment_notes.append(0)

            for j in range(start_segment_idx, end_segment_idx + 1):
                segment_notes[j] += 1

        total_segments += len(segment_notes)
        overlapping_segments += len(list(filter(lambda n: n > 1, segment_notes)))
    
    return overlapping_segments / total_segments    


def get_segmented_outputs(jam, segment_length):
    strings = jam.search(namespace="note_midi")
    num_segments = math.ceil(jam.file_metadata.duration / segment_length)
    segments = [[0, 0, 0, 0, 0, 0] for _ in range(num_segments)]

    MIDINote = namedtuple("SegmentedNote", ["time", "duration", "value"])

    num_overlaps = 0
     
    # Pour chaque corde
    for i, string_notes in enumerate(strings):
        # On commence par regrouper les notes par segments de 0.2s
        # Par exemple : [[{time: 0.04s, duration, value}, {time: 0.04s, duration, value}, {time: 0.04s, duration, value}], ...]
        # Remarque : une même note peut apparaître plusieurs fois, si elle a une intersection non-nulle avec plusieurs segments
        segment_notes = [[] for _ in range(num_segments)]
        for note in string_notes:
            start_segment_idx = math.floor(note.time / segment_length)
            end_segment_idx   = math.floor((note.time + note.duration) / segment_length)

            for j in range(start_segment_idx, end_segment_idx + 1):
                segment_notes[j].append(MIDINote(time=note.time % segment_length, duration=note.duration, value=note.value))

        num_overlaps += len(list(filter(lambda notes: len(notes) > 1, segment_notes)))

        # On passe ensuite de n notes par segment à 1 note par segment
        for j, notes in enumerate(segment_notes):
            if len(notes) > 0:
                segments[j][i] = round(notes[-1].value)
        
    print("Overlapping segments:", num_overlaps, "/", (6*num_segments), "(" + ("%.2f" % (100 * num_overlaps / (6*num_segments))) + "%)")

    # Conversion des notes en indice pour chaque frettes
    return [to_guitar_chords(segment) for segment in segments]

def to_guitar_chords(midi_values):
    # Initialize variables
    frets = np.zeros((6, 18), dtype=np.int32)
    
    # Retrieve all possible notes played
    for q in range(0, 6):
        qs = [40, 45, 50, 55, 59, 64]
        for f in range(0, 18):
            frets[q, f] = qs[q] + f

    tab = np.zeros((6, 19), dtype=np.int32)
    for t in range(0, len(midi_values)):
        note = int(midi_values[t])
        # Add a column at the beginning to indicate if no note is being played
        string = np.hstack(([1 if note == 0 else 0], (frets[t] == note) * 1))
        tab[t,:] = string

    # Convert to indices to save space in storage
    indices = np.where(tab == 1)[1]

    return indices

"""
output = np.copy(frets)
f_row = np.full((6, 6), np.inf)  # 6 strings with 1 note per string
f_col = np.full((6, 6), np.inf)

<code>

fcnt2 = 0

for t in range(0, len(midi_values)):
    fret_played = (frets == int(midi_values[t])) * 1

    cng = 0
    for dr in range(0, len(frets[:, 0])):
        for dc in range(0, len(frets[0, :])):
            if fret_played[dr, dc] == 1:
                if cng == 0:
                    fcnt2 = 0
                    cng += 1
                f_row[t, fcnt2] = dr
                f_col[t, fcnt2] = dc
                fcnt2 += 1

    print(fret_played)
print(f_row)
print(f_col)

# Initialize the 6 possible note solutions (one note per string)
f_sols = [np.copy(f_col) for _ in range(6)]

pri_cnt_c, = np.where(np.isfinite(f_col[0, :]))
pri_cnt_r, = np.where(np.isfinite(f_col[:, 0]))
print(pri_cnt_c)
print(pri_cnt_r)
for pri in range(0, len(pri_cnt_c)):
    for sub_r in range(1, 6):
        for sub_c in range(0, len(f_sols[0][0, :])):
            f_sols[pri][sub_r, sub_c] = abs(f_col[0, pri] - f_col[sub_r, sub_c])

if len(pri_cnt_r) == 0 or len(pri_cnt_c) == 0:
    true_tab = np.copy(np.zeros((6, 18), dtype=np.int32))
    print("tab", true_tab)
else:
    ck_sols = [np.zeros((len(pri_cnt_r) - 1, len(pri_cnt_c) - 1), dtype = np.int32) for _ in range(6)]
    sol_inds = [np.copy(ck_sols[0]) for _ in range(6)]

    # Replace infinite values with high finite values for each solution
    for ck_sol in range(6):
        for pri_sol_r in range(1, len(pri_cnt_r)):
            for pri_sol_c in range(0, len(pri_cnt_c) - 1):  # Random - 1
                infinites = np.isinf(f_sols[ck_sol][pri_sol_r, :]) 
                if np.any(infinites):
                    f_sols[ck_sol][pri_sol_r, np.argwhere(infinites)] = 999

                if ck_sol > 0:
                    ck_sols[ck_sol][0, pri_sol_c] = min(f_sols[ck_sol][pri_sol_r, :])

    # Determine "rating" for each solution
    tab_sols = [np.argmin(f_sols[i], axis = 1) for i in range(6)]
    min_sols = [np.min(f_sols[i], axis = 1) for i in range(6)]

    for i in range(6):
        inf = np.isinf(min_sols[i][:])
        if np.any(inf):
            min_sols[np.argwhere(inf)] = 0

    sols = [np.sum(min_sols[i][:]) for i in range(6)]

    print("sols:")
    print(sols)
"""

def visualize_overlap_frequencies(parsed_jams):
    import matplotlib.pyplot as plt

    # Average over the given jams
    f = lambda seg_len: sum(compute_overlap_frequency(jam, seg_len) for jam in parsed_jams) / len(parsed_jams)

    x = np.linspace(0.01, 0.2, num=20)
    y = np.vectorize(f)(x)
    plt.title("Note overlap (averaged over %d recordings)" % len(parsed_jams))
    plt.xlabel("Segment length (seconds)")
    plt.ylabel("% segments with more than 1 note")
    plt.plot(x, y)
    plt.show()

