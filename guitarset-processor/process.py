from process_annotations import get_annotation_files, get_segmented_outputs
from process_images import create_segmented_inputs
import csv
import os
import numpy as np
from time import time
from config import *

def output_index_csv(filename, rows):
    with open(os.path.join(PROCESSED_DIR, filename), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


def generate_dataset():
    n_files = 360

    print("Parsing annotations...")
    parsed_jams = get_annotation_files(n_files, ANNOTATIONS_DIR)

    #visualize_overlap_frequencies(parsed_jams[0:5])

    # Prepare outputs: for each jams file, get the outputs per segment
    print("Preparing outputs...")
    rows = [[] for j in range(len(RAW_AUDIO_DIRS))] # create one set of rows for each overlay dir
    rows_all = []

    for k,jam in enumerate(parsed_jams[0:n_files]):
        title = jam.file_metadata.title
        segmented_outputs = get_segmented_outputs(jam, SEGMENT_LENGTH)
        for i,segment_output in enumerate(segmented_outputs):
            formatted_segment_output = " ".join(segment_output.astype(str))
            # Create one entry for each variant of the input
            for j in range(len(RAW_AUDIO_DIRS)):
                rows[j].append([output_image_location(title, i, j), formatted_segment_output])
        print("[{0:.1f}".format(100 * (k+1) / n_files) + "%]", title, "\t\t\t", end="\r")

    # Output a main index with all the rows
    output_index_csv("index.csv", [r for rs in rows for r in rs])
    # Output individual index files for each overlay output
    for j in range(len(RAW_AUDIO_DIRS)):
        output_index_csv("index" + str(j) + ".csv", rows[j])
        # Also create the image dir
        os.makedirs(os.path.join(PROCESSED_DIR, str(j)), exist_ok=True)

    # Prepare inputs
    print("Preparing inputs...\t\t\t")
    for i,jam in enumerate(parsed_jams[0:n_files]):
        create_segmented_inputs(jam, SEGMENT_LENGTH, RAW_AUDIO_DIRS, PROCESSED_DIR)
        print("[{0:.1f}".format(100 * (i+1) / n_files) + "%]", jam.file_metadata.title, "\t\t\t", end="\r")
    print("Finished!", "\t" * 10)


def print_outputs(jam_name):
    import jams
    jam = jams.load(os.path.join(ANNOTATIONS_DIR, jam_name))
    outputs = [s.tolist() for s in get_segmented_outputs(jam, SEGMENT_LENGTH)]
    print("Chords for", jam_name + ":")
    print(outputs)


if __name__ == "__main__":
    generate_dataset() 
    #print_outputs("02_Funk2-119-G_solo.jams")
