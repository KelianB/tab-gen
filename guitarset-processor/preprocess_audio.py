from pydub import AudioSegment
from glob import glob 
from os import path
from config import *


# Fonction d'overlay d'une piste avec une seconde
def overlay(sound1, sound2, position):
    return sound1.overlay(sound2, position = position)


def create_overlay_files(input_files, output_dir, backgrounds_drum, backgrounds_bass):
    files_in = glob(input_files)
    N = len(files_in)
    print("Superposition de backgrounds sur", N, "fichiers...")
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
        output_name = path.join(output_dir, raw_file_name)
    
        # Créer le fichier fils
        output_sound = original_sound
        for b in backgrounds:
            output_sound = overlay(output_sound, b, 0)
        
        print("[{0:.1f}".format(100 * count / N) + "%]", raw_file_name, "\t\t\t", end="\r")
        output_sound.export(output_name, format="wav")

    print("Terminé.\t\t\t\t\t")


if __name__ == "__main__":
    # Import des différents backgrounds
    print("Import des backgrounds...")
    drums = ["drum1.mp3", "drum2.mp3"]
    backgrounds_drum = [AudioSegment.from_mp3(path.join(BACKGROUNDS_DIR, p)) for p in drums]

    bass = ["bass1.mp3", "bass2.mp3"]
    backgrounds_bass = [AudioSegment.from_mp3(path.join(BACKGROUNDS_DIR, p)) for p in bass]
    print("OK")

    # Superposition des sons
    create_overlay_files(DATASET_AUDIO_FILES, RAW_AUDIO_DIRS[1], backgrounds_drum, backgrounds_bass)
