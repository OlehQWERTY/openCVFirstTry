#controller
# import cv2
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
# frame = cv2.imread("_2__2018_09:23:47_pos_no_sole_OFF.PNG", 0)

	start_time = time.time()

	frame = Camera.takeFrame().copy()
	flag = mainWindow.show(frame)

	if(flag == 1): # proc only in case Space is pressed
		resizedImg = mainWindow.resize(frame)
		print('Processed img res: %s %s' % (resizedImg.shape[1], resizedImg.shape[0]))
		cor = findObj.find(resizedImg) # resized image
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

		ReadOrSaveImg.rw('W', 'IMGs/' + saveImgName + '.png', frame)  # save to img with imgName date + .png

		print('%s is saved' % saveImgName)

		elapsed_time = time.time() - start_time

		print("Iteration score: %f" % elapsed_time)



