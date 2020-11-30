from pydub import AudioSegment
import glob 

# fonction d'overlay d'une piste avec une seconde
def overlaying(sound1, sound2, position, output_name) :
    output = sound1.overlay(sound2, position = position)
    output.export(output_name, format="wav")


#path des morceaux du dataset (à modifier)
path1 = "guitarset-processor/raw/audioTest/*.*"
path2 = "background/overlayedDrums/*.*"

# importer les différents backgrounds
background_drum1 = AudioSegment.from_mp3("background/drum_background1.mp3")
background_drum2 = AudioSegment.from_mp3("background/drum_background2.mp3")

background_bass1 = AudioSegment.from_mp3("background/bass_background1.mp3")
background_bass2 = AudioSegment.from_mp3("background/bass_background2.mp3")


# fonctions d'overlay de l'ensemble des morceaux du path
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
        overlaying(original_sound, background, 0, overlayed_file_name)
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
        overlaying(original_sound, background, 0, overlayed_file_name)
        # print(overlayed_file_name)
        count += 1



# test
# massOverlayDrum(path1)
massOverlayBass(path2)
