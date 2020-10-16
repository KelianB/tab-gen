from process_annotations import get_annotation_files, get_segmented_outputs
from process_images import create_segmented_inputs
import csv
import os
import numpy as np

SEGMENT_LENGTH = 0.2 # 0.2s
RAW_AUDIO_DIR = "./raw/audio/"
ANNOTATIONS_DIR = "./raw/annotations/"
PROCESSED_DIR = "./processed/"

if __name__ == "__main__":    
    print("Parsing annotations...")
    parsed_jams = get_annotation_files(5, ANNOTATIONS_DIR)
    print("done.")

    #visualize_overlap_frequencies(parsed_jams[0:5])
    #print(to_guitar_chords([0, 51, 58, 0, 0, 70]))
    
    # Output a CSV file:
    # img_filename                  answer
    # 00_BN1-129-Eb_comp_mic_78     array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # 00_BN1-129-Eb_comp_mic_79     array([[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # ...

    rows = []
    for jam in parsed_jams[0:1]:
        img_name = jam.file_metadata.title
        # Prepare input
        create_segmented_inputs(jam, SEGMENT_LENGTH, RAW_AUDIO_DIR, PROCESSED_DIR)
        # Prepare output
        segmented_outputs = get_segmented_outputs(jam, SEGMENT_LENGTH)
        for i,segment_output in enumerate(segmented_outputs):
            # print(img_name + "_" + str(i) , segment_output)
            rows.append([img_name + "_" + str(i), np.array_str(segment_output)[1:-1]])
    
    with open(os.path.join(PROCESSED_DIR, "index.csv"), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
        