from chords import *


test = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 6, 0], 
[4, 6, 4, 6, 6, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 6, 0], [4, 0, 0, 0, 6, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 9, 0], [4, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0], [0, 0, 6, 1, 0, 0], [0, 11, 6, 0, 0, 0], [4, 0, 3, 6, 0, 0], 
[0, 0, 0, 6, 0, 0], [0, 0, 11, 6, 0, 0], [4, 0, 4, 0, 0, 0], [0, 0, 6, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 8, 0, 0, 0, 0], 
[0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [4, 0, 4, 3, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 3, 5, 0, 0], [0, 0, 0, 5, 0, 0], 
[4, 0, 4, 4, 3, 0], [4, 0, 4, 3, 3, 0], [0, 0, 8, 0, 0, 0], [4, 0, 4, 1, 0, 0], [0, 0, 0, 10, 0, 0], [0, 0, 0, 0, 6, 0], 
[0, 0, 0, 6, 6, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 11, 6], [0, 0, 0, 0, 7, 0], [4, 0, 0, 0, 6, 0], [0, 0, 0, 0, 9, 0], 
[0, 0, 0, 0, 6, 0], [0, 0, 0, 6, 6, 0], [4, 0, 4, 5, 2, 0], [0, 0, 0, 8, 0, 0], [4, 0, 4, 5, 4, 0], [0, 0, 0, 5, 1, 0], 
[0, 0, 0, 5, 0, 0], [4, 0, 4, 6, 0, 0], [0, 0, 0, 6, 0, 0], [0, 0, 0, 6, 0, 0], [4, 0, 0, 1, 0, 0], [0, 0, 3, 0, 0, 0], 
[0, 0, 3, 1, 0, 0], [4, 0, 3, 0, 0, 0], [0, 8, 0, 0, 0, 0], [0, 8, 3, 0, 0, 0], [4, 0, 4, 3, 3, 0], [0, 0, 0, 0, 0, 0], 
[0, 0, 4, 3, 0, 0], [0, 0, 0, 5, 0, 0], [4, 0, 4, 4, 3, 0], [4, 0, 4, 4, 3, 0], [0, 0, 8, 0, 0, 0], [4, 0, 4, 0, 0, 0], 
[0, 0, 6, 10, 0, 0], [0, 0, 0, 10, 6, 0], [0, 0, 0, 6, 6, 0], [0, 0, 0, 0, 11, 6], [0, 0, 0, 0, 7, 6], [0, 0, 0, 0, 7, 0], 
[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 10, 6, 0], [4, 0, 4, 6, 2, 0], [4, 0, 4, 4, 4, 0], 
[4, 0, 4, 5, 4, 0], [4, 0, 0, 5, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 4, 5, 0, 0], 
[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 7, 0], [0, 0, 0, 6, 5, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 6, 0], 
[0, 0, 7, 0, 0, 0], [3, 0, 4, 3, 0, 0], [0, 9, 4, 3, 2, 0], [0, 0, 11, 6, 0, 0], [3, 0, 4, 3, 2, 0], [4, 0, 4, 3, 0, 0], 
[4, 0, 4, 4, 3, 0], [0, 0, 0, 8, 0, 0], [0, 0, 0, 8, 0, 0], [4, 0, 4, 0, 4, 0], [0, 0, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 9], 
[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 9], [0, 0, 0, 0, 0, 9], [0, 0, 0, 0, 14, 0], [0, 0, 0, 0, 14, 9], [0, 4, 11, 0, 0, 0], 
[0, 4, 11, 0, 0, 0], [0, 4, 4, 0, 0, 0], [0, 0, 4, 0, 0, 4], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 9, 5, 0], 
[0, 0, 0, 6, 5, 0], [0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0], [3, 0, 4, 3, 0, 0], [3, 0, 4, 0, 2, 0], [0, 0, 4, 4, 2, 0], 
[0, 0, 4, 6, 2, 0], [3, 0, 4, 3, 0, 0], [4, 0, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0], 
[5, 0, 0, 0, 5, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 8, 0, 0], [0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0]]

test_2 = [[0, 1, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 2, 1], [0, 0, 0, 3, 2, 1], [0, 0, 0, 3, 2, 1], [0, 0, 0, 3, 2, 1], 
[0, 0, 0, 3, 2, 1], [0, 0, 0, 3, 2, 1], [0, 4, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 0, 0, 1, 2, 0], [0, 0, 3, 0, 0, 0], 
[0, 0, 1, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 4, 3], [0, 0, 0, 3, 0, 0]]


def generate_atex(allChords, filename = "mySong", songName = "Song name", artist = "Artist", tempo=100):
	finalChords = bestChords(allChords)
	f = open(filename + ".atex", "w")
	f.write(generate_metadata(songName, artist, tempo))
	f.write(generate_allChords(finalChords))
	f.close()
	print(finalChords)
	return


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



if __name__ == "__main__":

	generate_atex(test_2)
