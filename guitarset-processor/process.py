from process_annotations import get_annotation_files, get_segmented_outputs
from process_images import create_segmented_inputs
import csv
import os
import numpy as np
from time import time

# Configuration
SEGMENT_LENGTH = 0.2 # seconds
RAW_AUDIO_DIRS = ["./raw/audio/", "./raw/audio_overlay/"] # input variants
ANNOTATIONS_DIR = "./raw/annotations/"
PROCESSED_DIR = "./processed/"

if __name__ == "__main__":    
    n_files = 360

    print("Parsing annotations...")
    parsed_jams = get_annotation_files(n_files, ANNOTATIONS_DIR)

    #visualize_overlap_frequencies(parsed_jams[0:5])

    # Prepare outputs: for each jams file, get the outputs per segment
    print("Preparing outputs...")
    rows = []
    for jam in parsed_jams[0:n_files]:
        img_name = jam.file_metadata.title
        segmented_outputs = get_segmented_outputs(jam, SEGMENT_LENGTH)
        for i,segment_output in enumerate(segmented_outputs):
            formatted_segment_output = " ".join(segment_output.astype(str))
            # Create one entry for each variant of the input
            for j in range(len(RAW_AUDIO_DIRS)):
                rows.append([img_name + "_" + str(j) + "_" + str(i), formatted_segment_output])
    
    # Output to index.csv
    with open(os.path.join(PROCESSED_DIR, "index.csv"), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

    # Prepare inputs
    print("Preparing inputs...")
    start_time = time()
    for i,jam in enumerate(parsed_jams[0:n_files]):
        create_segmented_inputs(jam, SEGMENT_LENGTH, RAW_AUDIO_DIRS, PROCESSED_DIR)
        avg_time = (time() - start_time) / (i+1)
        remaining_time = (n_files - (i+1)) * avg_time
        print("[" + str(i+1).zfill(3) + "/" + str(n_files) + "]", "Generated images for", jam.file_metadata.title + ". Estimated time remaining:", int(remaining_time), "seconds.")       
    
    print("Finished!")
