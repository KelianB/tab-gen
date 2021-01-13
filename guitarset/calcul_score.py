from chords import *
import pandas as pd


def op_data(filename):
	col_list = ["name", "tab"]
	data = pd.read_csv(filename, usecols=col_list) 
	data['tab'] = data['tab'].map(lambda tab: strToLst(tab))

	return data


def strToLst(chord):
	new_list = chord.split(" ")
	new_list = list(map(int, new_list))
	if len(new_list)>6:
		new_list.pop()
	return new_list

def isEqualChord(chord1, chord2):
	possibilities = all_possibilities(chord1)
	return(chord2 in possibilities)

def calculateSimilarity(chord1, chord2):
	n = 0
	for i in range(len(chord1)):
		if chord1[i] == chord2[i]:
			n += 1
	return n / 6

def calculateScore(chord1, chord2):
	possibilities = all_possibilities(chord1)
	maxSim = 0

	for x in possibilities:
		sim = calculateSimilarity(x, chord2)
		if sim > maxSim:
			maxSim = sim

		if sim == 1:
			return 1

	return maxSim

def scores(index, output, n=54288):
	train = [0, 0]
	val = [0, 0]

	for i in range(n):
		if output["name"][i] == "train":
			train[0] += 1
			train[1] += calculateScore(index["tab"][i], output["tab"][i])

		if output["name"][i] == "val":
			val[0] += 1
			val[1] += calculateScore(index["tab"][i], output["tab"][i])

	return train, val



if __name__ == "__main__":


	testeur  = [0, 0, 3, 0, 0, 0]  #Une note seule
	testeur2 = [0, 1, 3, 3, 2, 1]  #Exemple d'accord jouable (LA mineur)
	testeur3 = [6, 8, 8, 6, 6, 0]  #Exemple d'entrée (à améliorer)
	testeur4 = [0, 4, 3, 1, 2, 1]  #Accord DO

	
	data1 = op_data("index.csv")
	data2 = op_data("output.csv")


	#print(isEqualChord(testeur2, testeur4))

	"""trainScore, valScore = scores(data1, data2)

	print(trainScore)
	print(valScore)

	trainScore = trainScore[1]/trainScore[0]
	valScore = valScore[1]/valScore[0]
	print(str(trainScore) + " " + str(valScore))"""
	print(all_possibilities(testeur3))
	#print(calculateScore(testeur2, testeur4))