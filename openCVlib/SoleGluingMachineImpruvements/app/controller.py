#controller

import sys
# sys.path.insert(0, '/app/models')
sys.path.append('models')
sys.path.append('./views')
# sys.path.append('../')



import barcode #barcode scaner
import findObj #findObject
from view import View
from webcam import WebCam
import imgRW
from settings import Settings
import motion
import time

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


WebCamParam = [640, 480, 15] # 160*120 - min HD - max
Camera = WebCam(0, WebCamParam[0], WebCamParam[1], WebCamParam[2])
mainWindow = View("MachineImprovements", WebCamParam[0], WebCamParam[1])
ReadOrSaveImg = imgRW.ImgRW()
flag = True


#
# movement detection init with the equal data
frame = Camera.takeFrame().copy()
MD = motion.MotionDetect(frame, frame)

while mainWindow.getWindowProperty() and flag: # while True:

	start_time = time.time()

	frame = Camera.takeFrame().copy()
	flag = mainWindow.draw(frame)

	# 11111111111111
	# MD.loadF1(img)
	#
	# img2 = cv2.imread('3.png', 1)
	# img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

	# print("F2: %f" % MD.loadF2(frame))

	if(MD.loadF2(frame) > 7): # wtf&
		print("movement %s" % str(time.time()))


	# hide square sole pos
	if flag == 2: # ord("s") set sole pos by mouse click - crop - and unclick
		mainWindow.kokokToZero()
		print("\'R\'")
	#

	# hide square sole pos
	if flag == 3:  # ord("d") default square (from settings file)
		mainWindow.loadDefaultSquare(frame, int(setStr[1][0]), int(setStr[1][1]), int(setStr[1][2]), int(setStr[1][3]))
		print("\'D\'")
	#

	if flag == 4: # save square pos (to settings)
		kok = mainWindow.returnRefPt()
		# print('12,45|'  + str(kok[0][0]) + ',' + str(kok[0][1]) + ',' + str(kok[1][0]) + ',' + str(kok[1][1]))
		Set.save('12,45|' + str(kok[0][0]) + ',' + str(kok[0][1]) + ',' + str(kok[1][0]) + ',' + str(kok[1][1])) # [(x1, y1), (x2, y2)])
		print("\'S\'")
	#



	if(flag == 1): # proc only in case Space is pressed
		# resizedImg = mainWindow.resizeImg(frame)
		# print('Processed img res: %s %s' % (resizedImg.shape[1], resizedImg.shape[0]))
		# cor = findObj.find(resizedImg) # resized image
		soleImg = mainWindow.returnSoleImg()
		cor = findObj.find(soleImg)  # sole image
		print('Processed sole res: %s %s' % (soleImg.shape[1], soleImg.shape[0]))
		isSoleStr = 'Sole'
		if not cor:
			# print("Empty!")
			# print(findObj.find(frame))
			pass
		else:
			# print(cor[0], cor[1])
			if cor[1] > 10: #and cor[0]/float(cor[1]) > 0.2: # check
				# print("Yes") # first (img - './1.png' or our image findObj.find(frame) ), second - './2.png'
				isSoleStr = 'NoSole' + '-' + str(cor[0]) + '/' + str(cor[1])
			else:
				# print("No")
				isSoleStr = 'Sole'

		# print(barcode.zbar(frame))
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


# 		11111111111111
	MD.loadF1(frame) # change first frame for movementDetection


