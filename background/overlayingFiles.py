from pydub import AudioSegment

sound1 = AudioSegment.from_mp3("background/summertime.mp3")
sound2 = AudioSegment.from_mp3("background/takefive.mp3")

# mix sound2 with sound1, starting at 5000ms into sound1)
output = sound1.overlay(sound2, position=5000)

# save the result
output.export("mixed_sounds.mp3", format="mp3")
