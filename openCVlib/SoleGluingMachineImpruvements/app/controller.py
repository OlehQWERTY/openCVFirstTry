#controller

import sys
import os # clear term func
import time

sys.path.append('models')
sys.path.append('./views')

import barcode #barcode scaner
import findObj #findObject
from view import View
from webcam import WebCam
import imgRW
from settings import Settings
import motion

import os
# chose an implementation, depending on os
if os.name == 'nt':  # sys.platform == 'win32':
	print("No gpio avaliable under windows!")
elif os.name == 'posix':
	print("RPI gpio init is done!")
	import gpio
else:
	raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)

# from gpiozero import LED
# from time import sleep
#
# out = LED(17)

# while True:
#     out.on()
#     sleep(1)
#     out.off()
#     sleep(1)

# img = cv2.imread('2.png', 1)
# img1 = cv2.imread('1.png', 1) #1
#
# img = cv2.resize(img, (img1.shape[1], img1.shape[0]))
# MD = motion.MotionDetect(img1, img)
# MD.loadF1(img)
#
# img2 = cv2.imread('3.png', 1)
# img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
# MD.loadF2(img2)

Set = Settings('1.set')
setStr = Set.load()

WebCamParam = [640, 360, 15] # 160*120 - min HD - max
Camera = WebCam(0, WebCamParam[0], WebCamParam[1], WebCamParam[2])
mainWindow = View("MachineImprovements", WebCamParam[0], WebCamParam[1])
ReadOrSaveImg = imgRW.ImgRW()
flag = True

#
# movement detection init with the equal data
frame = Camera.takeFrame().copy()
MD = motion.MotionDetect(frame, frame)
flagMovement = False
moveTime = 0

while mainWindow.getWindowProperty() and flag: # while True:

	start_time = time.time()

	frame = Camera.takeFrame().copy()
	flag = mainWindow.draw(frame) # number of pressed key


	# hide square sole pos
	if flag == 2: # ord("s") set sole pos by mouse click - crop - and unclick
		mainWindow.mousePosToZero()
		print("\'R\'" + ' ' + "Reset current square")
	#

	# hide square sole pos
	if flag == 3:  # ord("d") default square (from settings file)
		mainWindow.loadDefaultSquare(frame, int(setStr[1][0]), int(setStr[1][1]), int(setStr[1][2]), int(setStr[1][3]))
		print("\'D\'" + ' ' + "Download square pos from set file")
	#

	if flag == 4: # save square pos (to settings)
		kok = mainWindow.returnRefPt()
		if kok != 0:
			Set.save('12,45|' + str(kok[0][0]) + ',' + str(kok[0][1]) + ',' + str(kok[1][0]) + ',' + str(kok[1][1])) # [(x1, y1), (x2, y2)])
			print("\'S\'" + ' ' + "Save square")
		else:
			print("Nothing to save!")
	#

	if flag == 5: # turn on/off movement detection
		flagMovement = not flagMovement
		print("\'M\'" + " " + str(flagMovement))
		# print(chr(27) + "[2J") # clear terminal maybe in linux
		os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

		if 'soleImg' in locals():
			MD.loadF1(soleImg)  # load zone
			MD.loadF2(soleImg)  # load zone
		else:
			MD.loadF1(frame)  # load zone
			MD.loadF2(frame)  # load zone

	if flagMovement:
		if 'soleImg' in locals():
			movementStr = MD.loadF2(soleImg)  # frame
		else:
			movementStr = MD.loadF2(frame)  # frame

		if movementStr == -1: # not 5 iteration passed
			continue
		elif movementStr == 1: # movement detected
			moveTime = time.time()
			print("Movement! %s" % moveTime)
			continue
		elif movementStr == 0: # movement not detected
			if (time.time() - moveTime) > 0.5:
		# 		print("Ready!")
				pass



	if(flag == 1): # proc only in case Space is pressed
		soleImg = mainWindow.returnSoleImg()
		cor = findObj.find(soleImg)  # sole image
		print('Processed sole res: %s %s' % (soleImg.shape[1], soleImg.shape[0]))
		isSoleStr = 'Sole'
		if not cor:
			pass
		else:
			if cor[1] > 10: # and cor[0]/float(cor[1]) > 0.2: # check
				isSoleStr = 'NoSole' + '-' + str(cor[0]) + '/' + str(cor[1])
			else:
				isSoleStr = 'Sole'

		barCodeData = barcode.zbar(frame)

		if barCodeData is None:
			barCodeData = ['No', 'No']

		localTime = time.localtime(time.time())
		saveImgName = str(localTime[2]) + '-' + str(localTime[1]) + '-' \
					  + str(localTime[0]) + '-' + str(localTime[3]) + '-' + str(localTime[4]) + '-' \
					  + str(localTime[5]) + '-' + isSoleStr + '-' + 'QR' + '-' + str(barCodeData[1])  # 'IMGs/' +

		ReadOrSaveImg.rw('W', '../IMGs/' + saveImgName + '.png', frame)  # save to img with imgName date + .png

		print('%s is saved' % saveImgName)

		elapsed_time = time.time() - start_time

		print("Iteration score: %f" % elapsed_time)

		# if len(mainWindow.refPt) == 2:
		# 	print(mainWindow.refPt)

		print(mainWindow.returnRefPt())