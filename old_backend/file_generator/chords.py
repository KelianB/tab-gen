from constraint import *
import time


def generate_possibilities_one_string(chord_initial):
	possibilities = [chord_initial]
	#corde 0
	if chord_initial[0] != 0:
		if chord_initial[0] > 5:
			possibilities.append([0,chord_initial[0]-5,0,0,0,0])
		if chord_initial[0] > 10:
			possibilities.append([0,0,chord_initial[0]-10,0,0,0])
		if chord_initial[0] > 15:
			possibilities.append([0,0,0,chord_initial[0]-15,0,0])
		return possibilities

	#corde 1
	if chord_initial[1] != 0: 
		if chord_initial[1]+5<19: #vers corde 0
			possibilities.append([chord_initial[1]+5,0,0,0,0,0])
		if chord_initial[1] > 5:  #vers corde 2
			possibilities.append([0,0,chord_initial[1]-5,0,0,0])
		if chord_initial[1] > 10:  #vers corde 3
			possibilities.append([0,0,0,chord_initial[1]-10,0,0])
		if chord_initial[1] > 14:  #vers corde 4
			possibilities.append([0,0,0,0,chord_initial[1]-14,0])
		return possibilities

	#corde 2
	if chord_initial[2] != 0: 
		if chord_initial[2]+10<19: #vers corde 0
			possibilities.append([chord_initial[2]+10,0,0,0,0,0])
		if chord_initial[2]+5<19: #vers corde 1
			possibilities.append([0,chord_initial[2]+5,0,0,0,0])
		if chord_initial[2] > 5:  #vers corde 3
			possibilities.append([0,0,0,chord_initial[2]-5,0,0])
		if chord_initial[2] > 9:  #vers corde 4
			possibilities.append([0,0,0,0,chord_initial[2]-9,0])
		if chord_initial[2] > 14:  #vers corde 5
			possibilities.append([0,0,0,0,0,chord_initial[2]-14])
		
		return possibilities

	#corde 3
	if chord_initial[3] != 0: 
		if chord_initial[3]+15<19: #vers corde 0
			possibilities.append([chord_initial[3]+15,0,0,0,0,0])
		if chord_initial[3]+10<19: #vers corde 1
			possibilities.append([0,chord_initial[3]+10,0,0,0,0])
		if chord_initial[3]+5<19: #vers corde 2
			possibilities.append([0,0,chord_initial[3]+5,0,0,0])


		if chord_initial[3] > 4:  #vers corde 4
			possibilities.append([0,0,0,0,chord_initial[3]-4,0])
		if chord_initial[3] > 9:  #vers corde 5
			possibilities.append([0,0,0,0,0,chord_initial[3]-9])
		
		return possibilities


	#corde 4
	if chord_initial[4] != 0: 
		if chord_initial[4]+14<19: #vers corde 1
			possibilities.append([0,chord_initial[4]+14,0,0,0,0])
		if chord_initial[4]+9<19: #vers corde 2
			possibilities.append([0,0,chord_initial[4]+9,0,0,0])
		if chord_initial[4]+4<19: #vers corde 3
			possibilities.append([0,0,0,chord_initial[4]+4,0,0])


		if chord_initial[4] > 5:  #vers corde 5
			possibilities.append([0,0,0,0,0,chord_initial[4]-5])
		
		return possibilities


	#corde 5
	if chord_initial[5] != 0: 
		if chord_initial[5]+14<19: #vers corde 2
			possibilities.append([0,0,chord_initial[5]+14,0,0,0])
		if chord_initial[5]+9<19: #vers corde 3
			possibilities.append([0,0,0,chord_initial[5]+9,0,0])
		if chord_initial[5]+5<19: #vers corde 4
			possibilities.append([0,0,0,0,chord_initial[5]+5,0])
		
		return possibilities

	
	return possibilities


def differents_max(c0, c1, c2, c3, c4, c5):

	poss = [c0, c1, c2, c3, c4, c5]
	poss = [x for x in poss if x != [0,0,0,0,0,0]]
	indexes = [x.index(max(x)) for x in poss]

	if len(indexes) > len(set(indexes)):
		return False
	else:
		return True
   


def contraintes(chord):

	n0 = generate_possibilities_one_string([chord[0],0,0,0,0,0])
	n1 = generate_possibilities_one_string([0,chord[1],0,0,0,0])
	n2 = generate_possibilities_one_string([0,0,chord[2],0,0,0])
	n3 = generate_possibilities_one_string([0,0,0,chord[3],0,0])
	n4 = generate_possibilities_one_string([0,0,0,0,chord[4],0])
	n5 = generate_possibilities_one_string([0,0,0,0,0,chord[5]])


	problem = Problem()
	problem.addVariable("c0", n0)
	problem.addVariable("c1", n1)
	problem.addVariable("c2", n2)
	problem.addVariable("c3", n3)
	problem.addVariable("c4", n4)
	problem.addVariable("c5", n5)
	problem.addConstraint(lambda a, b, c, d, e, f: differents_max(a,b,c,d,e,f), ["c0", "c1", "c2", "c3", "c4", "c5"])
	
	return problem.getSolutions()

def economy_score2(chord):
	"""This version calculate the score related to the distance between the frets played and the end of the handle
	For example, a chord close to the handle will get a low score."""

	score = 0
	strings_played = [x for x in chord if x > 0] 
	if len(strings_played) > 1:
		if 0 in chord[1:5]:
			score += 1

	frets_played = [x for x in chord if x > 1] 
	if len(frets_played) == 0:
		return score
	for finger in frets_played:
		score += 1 + (abs(frets_played[0] - finger)) + finger


	return score

def recompose(allChords):
	chords = []
	for elem in allChords:
		chords.append([sum(x) for x in zip(elem["c0"], elem["c1"], elem["c2"], elem["c3"], elem["c4"], elem["c5"])])

	return chords

def show_scores(chord):
	poss = recompose(contraintes(chord))
	toString = ""
	for i in poss:
		toString += str(i) + ", score : " + str(economy_score2(i)) + '\n'

	return toString

def all_possibilities(chord):
	poss = recompose(contraintes(chord))

	return poss


def bestChord(chord):

	poss = recompose(contraintes(chord))
	best_one = poss[0]
	for p in poss:
		if economy_score2(p)<economy_score2(best_one):
			best_one = p

	return best_one

def bestChords(allChords):

	new_chords = [bestChord(x) for x in allChords]
	return new_chords


if __name__ == "__main__":

	testeur  = [0, 0, 3, 0, 0, 0]  #Une note seule
	testeur2 = [0, 1, 3, 3, 2, 1]  #Exemple d'accord jouable (LA mineur)
	testeur3 = [6, 8, 8, 6, 6, 0]  #Exemple d'entrée (à améliorer)
	testeur4 = [0, 4, 3, 1, 2, 1]  #Accord DO

	
	print(all_possibilities(testeur2))	




