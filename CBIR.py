import cv2
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
import imghdr
from operator import itemgetter
from math import *

def getImageDistance(folder, originalImage):
	# Create dictionnary
	dictionnaryColorCompare = {}
	dictionnaryTextureCompare = {}
	# Get open initial image
	imgInit = openImage(folder, originalImage)
	# Get histogram initial image
	initHistogram = getHistImage(imgInit) 
	# Get matrice occurrence
	matricesInit = getCooccurrence(imgInit)
	initEnergie, initInertie, initEntropie, initMoment = calculCooccurence(matricesInit)

	for filename in os.listdir(folder):
		# Open image
		img = openImage(folder, filename)
		# If it's an image and not if it's not the initial image
		if (imghdr.what(folder + "/" + filename) is not None) and (filename != originalImage):
			# Get histogram
			currentHist = getHistImage(img)
            # Compare botn images
			value = compareColor(initHistogram, currentHist)
			# Put values in a dictionnary
			dictionnaryColorCompare[filename] = value[0]

			# Compare by texture
			matrices = getCooccurrence(img)
			energie, inertie, moment, entropie = calculCooccurence(matrices)
			resTexture = distanceCooccurence(initEnergie, initInertie, initEntropie, initMoment, energie, inertie, entropie, moment)
			# Put values in a dictionnary
			dictionnaryTextureCompare[filename] = resTexture

	finalDictionary = {}
	# Sort similarity table
	for key, value in dictionnaryColorCompare.items():
		finalDictionary[key] = (value*0.5) + (dictionnaryTextureCompare[key]*0.5)

	tabKey = []		
	tabValue = [] 
	for key, value in sorted(finalDictionary.iteritems(), key=lambda (k,v): (v,k)):
		tabKey.append(key)
		tabValue.append(value)

	return (tabKey, tabValue)

# Return image opened
def openImage(folder,filename):
	return cv2.imread(os.path.join(folder,filename))

# Return the 3 histogram RGB
def getHistImage(img):
	histBlue = cv2.calcHist([img],[0],None,[16],[0,256])
	histGreen = cv2.calcHist([img],[1],None,[16],[0,256])
	histRed = cv2.calcHist([img],[2],None,[16],[0,256])
	return [histBlue, histGreen, histRed]

# Compare two images
def compareColor(initHistogram, currentHist):
	dividende = 0
	diviseur = 0

	for i, initHistColor in enumerate(initHistogram):
		currentHistColor = currentHist[i]
		for j, initElement in enumerate(initHistColor):
			currentElement = currentHistColor[j]
			dividende += abs(initElement - currentElement)
			diviseur += initElement
	return dividende/diviseur

# Convert rgb img in gray
def rgb2gray(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

# Get cooccurrence 
def getCooccurrence(currentImg):
	# Convert to gray image 
	currentGrayImg = rgb2gray(currentImg)

	# Get width and height
	width, height = currentGrayImg.shape
	width = width - 1
	height = height - 1
	sizeCooccurrence = 8

	# Create new matrice
	newMatrice = np.zeros(shape=(width,height))

	# Only 8 possible values
	for p in range(0, width):
		for q in range(0, height):
			newMatrice[p, q] = (currentGrayImg[p, q] * sizeCooccurrence ) // 256

	# Create cooccurrence matrices
	cooccurrence1 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence2 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence3 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence4 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence5 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence6 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence7 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))
	cooccurrence8 = np.zeros(shape=(sizeCooccurrence, sizeCooccurrence))

	# Distance = 1 for all directions
	direction = [[1,0],[1,1],[0,1],[-1,1]]
	index = 0
	for dx, dy in direction:
		for p in range(0, width-1):
			for q in range(0, height-1):
				if(newMatrice[p, q] != newMatrice[p + dx, q + dy] and (p < width-dx or q < height-dy or p > dx or q > dy)):
					if(index == 0):
						cooccurrence1[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
					if(index == 1):
						cooccurrence2[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
					if(index == 2):
						cooccurrence3[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
					if(index == 3):
						cooccurrence4[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
		index += 1

	# Distance 2 for all directions
	direction = [[2,0],[2,2],[0,2],[-2,2]]
	index = 0
	for dx, dy in direction:
		for p in range(0, width-2):
			for q in range(0, height-2):
				if(newMatrice[p, q] != newMatrice[p + dx, q + dy] and (p < width-dx or q < height-dy or p > dx or q > dy)):
					if(index == 0):
						cooccurrence5[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
					if(index == 1):
						cooccurrence6[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
					if(index == 2):
						cooccurrence7[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
					if(index == 3):
						cooccurrence8[int(newMatrice[p, q]), int(newMatrice[p + dx, q + dy])] += 1
		index += 1

	# Normalization of matrice
	cooccurrence1 = cooccurrence1 / width*height
	cooccurrence2 = cooccurrence2 / width*height
	cooccurrence3 = cooccurrence3 / width*height
	cooccurrence4 = cooccurrence4 / width*height
	cooccurrence5 = cooccurrence5 / width*height
	cooccurrence6 = cooccurrence6 / width*height
	cooccurrence7 = cooccurrence7 / width*height
	cooccurrence8 = cooccurrence8 / width*height

	# Add to tab
	tabCooccurence = []
	tabCooccurence.append(cooccurrence1)
	tabCooccurence.append(cooccurrence2)
	tabCooccurence.append(cooccurrence3)
	tabCooccurence.append(cooccurrence4)
	tabCooccurence.append(cooccurrence5)
	tabCooccurence.append(cooccurrence6)
	tabCooccurence.append(cooccurrence7)
	tabCooccurence.append(cooccurrence8)

	return tabCooccurence

# Calcul de l'energie, inertie, entropie et moment
def calculCooccurence(currentCooccurence):
	energie = 0
	inertie = 0
	entropie = 0
	moment = 0
	size = 8

	# Energie
	for matrice in currentCooccurence:
		for i in range(0, size):
			for j in range(0, size):
				energie += matrice[i, j]**2 
	# Inertie
	for matrice in currentCooccurence:
		for i in range(0, size):
			for j in range(0, size):
				inertie += (i-j)**2 * matrice[i, j]

	# Entropie
	# for matrice in currentCooccurence:
	# 	for i in range(0, size):
	# 		for j in range(0, size):
	# 			entropie += - (matrice[i, j] * (np.log(matrice[i, j])))

	# Moment differentiel inverse
	for matrice in currentCooccurence:
		for i in range(0, size):
			for j in range(0, size):
				moment += (1 / (1 + (matrice[i, j])**2)) * matrice[i, j]

	# print energie
	# print inertie
	# print entropie
	# print moment

	return energie, inertie, moment, entropie

# Calcul de distance de cooccurrence
def distanceCooccurence(initEnergie, initInertie, initEntropie, initMoment, energie, inertie, entropie, moment):
	return (sqrt(((initEnergie-energie)**2) + ((initInertie-inertie)**2) + ((initMoment-moment)**2) )) / 3 #4 + ((initEntropie-entropie)**2) 

# Get image name & get bdd
imgPath = str(sys.argv[1])
CBIR_BDD = str(sys.argv[2])

# Get dictionnary of distance
dictionnaryKey, dictionnaryValue = getImageDistance(CBIR_BDD, imgPath)

# Print top 10 images
print "Voici les images ressemblant le plus a l'image " + imgPath

# Init CBIR_BDD_2
# python CBIR.py obj1__50.png CBIR_BDD_2
# topImage = 60
# objOK = 0
# objTotalImageInBDD = 72
# TotalImageInBDD = 7200

# Init CBIR_BDD
# python CBIR.py obj1__50.png CBIR_BDD
topImage = 5
objOK = 0
objTotalImageInBDD = 5
TotalImageInBDD = 15

# Precision
precision = 0

for x in range(0, topImage):
	print (str(dictionnaryKey[x]) + " : " + str(dictionnaryValue[x]))
	nameObj = dictionnaryKey[x].split('__')
	if imgPath.split('__')[0] == nameObj[0]:
		objOK += 1

print ""
print "Image(s) retournee(s) correcte(s) = " + str(objOK)
print "Images retournees = " + str(topImage)
print "Image total =", TotalImageInBDD
print "Nombre total d'image correcte(s) present dans la base de donnees =", objTotalImageInBDD
