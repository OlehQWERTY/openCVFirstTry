#controller
# import cv2

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
import time


WebCamParam = [640, 480, 15] # 160*120 - min HD - max
Camera = WebCam(0, WebCamParam[0], WebCamParam[1], WebCamParam[2])
mainWindow = View("MachineImprovements", WebCamParam[0], WebCamParam[1])
ReadOrSaveImg = imgRW.ImgRW()
flag = True


while mainWindow.getWindowProperty() and flag: # while True:

	# hide square sole pos
	if flag == 2: # ord("s") set sole pos by mouse click - crop - and unclick
		mainWindow.kokokToZero()
		print("\'S\'")
	#

	start_time = time.time()

	frame = Camera.takeFrame().copy()
	flag = mainWindow.draw(frame)

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
			if cor[1] > 10: #and cor[0]/float(cor[1]) > 0.2: # cheak
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


