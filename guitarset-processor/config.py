# Chemins
BACKGROUNDS_DIR = "./backgrounds" 
DATASET_AUDIO_FILES = "./raw/audio/*.wav"
RAW_AUDIO_DIRS = ["./raw/audio/", "./raw/audio_overlay/"] # input variants
ANNOTATIONS_DIR = "./raw/annotations/"
PROCESSED_DIR = "./processed/"

AUDIO_SAMPLE_RATE = 44100 # Hz

# Whether or not to replace the pre-existing images when generating new ones
OVERWRITE_IMAGES = False 

# Configuration
SEGMENT_LENGTH = 0.2 # seconds

def output_image_location(title, segment_index, overlay_index):
    return str(overlay_index) + "/" + title + "_" + str(segment_index) + ".png"
