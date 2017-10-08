import sys
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import imghdr

def getImageDistance(folder, originalImage):
	# Create dictionnary
	dictionnaryColorCompare = {}
	# Get open initial image
	imgInit = openImage(folder, originalImage)
	# Get histogram initial image
	initHistogram = getHistImage(imgInit) 

	# Explore all images of the BDD and analyze them
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
            # Close img
            # Don't know how to do it

    # Sort similarity table
	tabKey = []		
	tabValue = [] 
	for key, value in sorted(dictionnaryColorCompare.iteritems(), key=lambda (k,v): (v,k)):
		tabKey.append(key)
		tabValue.append(value)

	# Return table of values
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


# Get image name & get bdd
# Line : python colorCBIR.py obj1__30.png CBIR_BDD_2
imgPath = str(sys.argv[1])
CBIR_BDD = str(sys.argv[2])

# Get dictionnary of distance
dictionnaryKey, dictionnaryValue = getImageDistance(CBIR_BDD, imgPath)

# Print top 10 images
print "Voici les images ressemblant le plus a l'image " + imgPath

# Init CBIR_BDD_2
# python colorCBIR.py obj1__50.png CBIR_BDD_2
# topImage = 60
# objOK = 0
# objTotalImageInBDD = 72
# TotalImageInBDD = 7200

# Init CBIR_BDD
# python colorCBIR.py obj1__50.png CBIR_BDD
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
