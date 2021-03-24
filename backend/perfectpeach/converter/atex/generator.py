from .chords import *

def generate_atex(allChords, songName = "Song name", artist = "Artist", tempo=100):
	finalChords = bestChords(allChords)
	metadata = generate_metadata(songName, artist, tempo)
	chords = generate_allChords(finalChords)
	return metadata + chords

def generate_metadata(songName, artist, tempo):
	text = r'\title ' + r'"' + songName + r'"' + "\n" + \
	r'\subtitle ' + r'"' + artist + r'"' + "\n" + \
	r'\tempo ' + str(tempo) + "\n.\n" + \
	r'\track "Guitar"' + "\n" + \
	r'    \staff{tabs} \instrument 24' + "\n\n" 

	return text

def generate_allChords(allChords):
	string = ""
	count = 0
	for chord in allChords:
		string += generate_chord(chord) + '.8 '
		count += 1
		if count == 8 :
			string += "|\n"
			count = 0

	return string

def generate_chord(chord):

	if chord == [0,0,0,0,0,0]:
		string = "r"
		return string

	strings_played = [x for x in chord if x > 0]
	if len(strings_played) > 1:
		string = ""
		count = 6
		for keys in chord:
			if keys != 0:
				string += str(keys-1) + '.' + str(count) + ' '
			count -= 1
		string = "(" + string[0:-1] + ")"

	else:
		chord = list(reversed(chord))
		string = str(max(chord)-1) + '.' + str(chord.index(max(chord))+1)

	return string

