from pydub import AudioSegment
import glob 

"""
# mix sound2 with sound1, starting at 5000ms into sound1)
output = sound1.overlay(sound2, position=5000)
# save the result
output.export("mixed_sounds.mp3", format="mp3") """


def overlaying(sound1, sound2, position, output_name) :
    output = sound1.overlay(sound2, position=position)
    output.export(output_name, format="mp3")





# TEST ZONE
sound1 = AudioSegment.from_mp3("background/summertime.mp3")

sound2 = AudioSegment.from_mp3("background/takefive.mp3")

overlaying(sound1, sound2, 500, "test.mp3")