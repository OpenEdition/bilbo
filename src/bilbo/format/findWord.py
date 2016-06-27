# -*- coding: utf-8 -*-

def prevNext(wordList, word, wordCount):
	if (word in wordList):
		index = wordList.index(word)
		taille = len(wordList)
		offsetDebut = offsetFin = 0

		debut = index-wordCount
		if (debut<0):
			offsetDebut = abs(debut)
			debut = 0
		listDebut = [False for x in range(offsetDebut)]

		fin = index+wordCount+1
		if fin >= taille:
			offsetFin = fin - taille
			fin = taille
		listFin = [False for x in range(offsetFin)]

		return listDebut + wordList[debut:fin] + listFin
	return []


laListe = ['il', 'faut', 'que', 'je', 'cherche', 'un', 'mot', 'dans', 'cette', 'liste', 'et', 'que', 'je', 'trouve', 'les', 'x', 'occurences', 'autour']

print 'cherche, 2 :'
print prevNext(laListe, 'cherche', 2)
print 'cherche, 0 :'
print prevNext(laListe, 'cherche', 0)
print 'faut,2  :'
print prevNext(laListe, 'faut', 2)
print 'occurences, 5 :'
print prevNext(laListe, 'occurences', 5)
print 'arnaud, 2 :'
print prevNext(laListe, 'arnaud', 2)

