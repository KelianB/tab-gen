from pydub import AudioSegment
from glob import glob 
from os import path

# Chemins
BACKGROUNDS_DIR = "./backgrounds" 
INPUT_FILES = "./raw/audio_test_temporary/*.wav"
OUTPUT_DIR = "./raw/audio_overlay/"


# Fonction d'overlay d'une piste avec une seconde
def overlay(sound1, sound2, position):
    return sound1.overlay(sound2, position = position)


def create_overlay_files(input_files, backgrounds_drum, backgrounds_bass):
    # Overlay de chaque fichier avec les backgrounds en alternance
    for count, file in enumerate(glob(input_files)):
        original_sound = AudioSegment.from_wav(file)

        n_drum = count % 3
        n_bass = (count + 1) % 3

        backgrounds = []
        # 1 fichier sur 3 n'aura pas de drum
        if n_drum != 2:
            backgrounds.append(backgrounds_drum[n_drum])
        # Idem pour la basse
        if n_bass != 2:
            backgrounds.append(backgrounds_bass[n_bass])
        
        # Nommer le fichier fils
        raw_file_name = file.split("\\",1)[1]
        output_name = path.join(OUTPUT_DIR, raw_file_name)
    
        # Créer le fichier fils
        output_sound = original_sound
        for b in backgrounds:
            output_sound = overlay(output_sound, b, 0)
        
        print("Export du fichier", output_name)
        output_sound.export(output_name, format="wav")


if __name__ == "__main__":
    # Import des différents backgrounds
    print("Import des backgrounds...")
    backgrounds_drum_names = ["drum1.mp3", "drum2.mp3"]
    backgrounds_drum = [AudioSegment.from_mp3(path.join(BACKGROUNDS_DIR, p)) for p in backgrounds_drum_names]

    backgrounds_bass_names = ["bass1.mp3", "bass2.mp3"]
    backgrounds_bass = [AudioSegment.from_mp3(path.join(BACKGROUNDS_DIR, p)) for p in backgrounds_bass_names]
    print("OK")

    create_overlay_files(INPUT_FILES, backgrounds_drum, backgrounds_bass)



# fonctions d'overlay de l'ensemble des morceaux du path
"""
def massOverlayDrum(path) :
    count = 0
    # overlay de chaque fichier avec un des backgrounds en alternance
    for file in glob.glob(path) :
        original_sound = AudioSegment.from_wav(file)
        if (count % 2 == 0 ) :
            background = background_drum1
            backing_name = "1"
        else :
            background = background_drum2
            backing_name = "2"
        # nommer le fichier fils
        raw_file_name = file.split("\\",1)[1]
        overlayed_file_name = "background/overlayedDrums/%s_overlay%s.wav" %(raw_file_name.split(".wav",1)[0], backing_name)
        # créer le fichier fils
        overlay(original_sound, background, 0, overlayed_file_name)
        # print(overlayed_file_name)
        count += 1

def massOverlayBass(path) :
    count = 0
    # overlay de chaque fichier avec un des backgrounds en alternance
    for file in glob.glob(path) :
        original_sound = AudioSegment.from_wav(file)
        if (count % 2 == 0 ) :
            background = background_bass1
            backing_name = "1"
        else :
            background = background_bass2
            backing_name = "2"
        # nommer le fichier fils
        raw_file_name = file.split("\\",1)[1]
        overlayed_file_name = "background/overlayedDrumsAndBass/%s_overlay%s.wav" %(raw_file_name.split(".wav",1)[0], backing_name)
        # créer le fichier fils
        overlay(original_sound, background, 0, overlayed_file_name)
        # print(overlayed_file_name)
        count += 1
"""
