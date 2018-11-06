#controller
# import cv2
import barcode #barcode scaner
import findObj #findObject
from view import View
from webcam import WebCam
import time

WebCamParam = [640, 480, 15] # 160*120 - min HD - max
Camera = WebCam(0, WebCamParam[0], WebCamParam[1], WebCamParam[2])
mainWindow = View("MachineImprovements", WebCamParam[0], WebCamParam[1])
flag = True
while mainWindow.getWindowProperty() and flag: # while True:
# frame = cv2.imread("_2__2018_09:23:47_pos_no_sole_OFF.PNG", 0)

	start_time = time.time()

	frame = Camera.takeFrame().copy()
	flag = mainWindow.show(frame)

	if(flag == 1): # proc only in case Space is pressed
		cor = findObj.find(frame)
		if not cor:
			# print("Empty!")
			# print(findObj.find(frame))
			pass
		else:
			# print(cor[0], cor[1])
			if cor[1] > 10 and cor[0]/float(cor[1]) > 0.2:
				print("Yes") # first (img - './1.png' or our image findObj.find(frame) ), second - './2.png'
			else:
				print("No")

		print(barcode.zbar(frame))

	elapsed_time = time.time() - start_time
	# print("Iteration score: %f" % elapsed_time)

