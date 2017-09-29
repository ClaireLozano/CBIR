import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import imghdr
from operator import itemgetter

def load_images_from_folder(folder, initHistogram, originalImage):
	# Le dictionnaire qui contiendra les differents nom des images ainsi que leur valeur 
	dictionnary = {}
	imgInit = openImage(folder, originalImage)
	for filename in os.listdir(folder):
		print filename
		img = openImage(folder, filename)
		if (imghdr.what(folder + "/" + filename) is not None) and (filename != originalImage):
			# Get histogram
			currentHist = getHistImage(img)

            # Compare by color
			value = compareColor(initHistogram, currentHist)
			# Compare by texture
			valueTexture = compareTexture(img)

		    # Put values in a dictionnary
			dictionnary[filename] = value[0]

            # Close img

    # Sort similarity table
	tabKey = []		
	tabValue = [] 
	for key, value in sorted(dictionnary.iteritems(), key=lambda (k,v): (v,k)):
		#print "%s: %s" % (key, value)
		tabKey.append(key)
		tabValue.append(value)
	return (tabKey, tabValue)

def openImage(folder,filename):
	return cv2.imread(os.path.join(folder,filename))

def getHistImage(img):
	histBlue = cv2.calcHist([img],[0],None,[16],[0,256])
	histGreen = cv2.calcHist([img],[1],None,[16],[0,256])
	histRed = cv2.calcHist([img],[2],None,[16],[0,256])
	return [histBlue, histGreen, histRed]

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

def rgb2gray(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)


def compareTexture(currentImg):
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
	
	return 0


# Open original image
imgPath = "CBIR_BDD/obj1__50.png"
name = imgPath.split('/')
img = openImage(name[0],name[1])

# Get histogram
initHistogram = getHistImage(img) 
CBIR_BDD = "CBIR_BDD"

# Get dictionnary
dictionnaryKey, dictionnaryValue = load_images_from_folder(CBIR_BDD, initHistogram, name[1])

# Sorted dictionnary
print(dictionnaryKey)
#print(dictionnaryValue)
