# pip install -U scikit-learn

#usage
# python color_mask.py --image maxresdefault.jpg 

import numpy as np
import argparse
import cv2
import time
 

timer1 = time.time()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
 
image = cv2.imread(args["image"])

# h, w, _ = image.shape # aspect ratio
rH = 120
rW = 160
resizedImg = cv2.resize(image, (rW,rH))


sensitivity = 20
pxAmmount = rW * rH * 3
for x in range(rH):
	for y in range(rW):
		for z in range(3):
			if((resizedImg[x][y][z]%sensitivity) != 0):
				resizedImg[x][y][z] = int(resizedImg[x][y][z]/sensitivity)*sensitivity
colourArr = []

for x in range(int(rH/20)):
	blue = 0
	red = 0
	green = 0
	for y in range(rW):
		# for z in range(3):
		blue += resizedImg[x*20][y][0]
		red += resizedImg[x*20][y][1]
		green += resizedImg[x*20][y][2]
	blue = int(blue/rW)
	red = int(red/rW)
	green = int(green/rW)
	colourArr.append([blue,red,green])

print(colourArr)

img = np.zeros((600,100,3), np.uint8)
for i in range(6):
	cv2.circle(img,(50,50+100*i), 50, (colourArr[i][0],colourArr[i][1],colourArr[i][2]), -1)

cv2.imshow("b", img)

resizedImgToShow = cv2.resize(resizedImg, (640, 480))

cv2.imshow("Image", resizedImgToShow)


timer2 = time.time() - timer1

print(timer2)

cv2.waitKey(0)
