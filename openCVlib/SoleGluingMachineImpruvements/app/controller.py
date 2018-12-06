# controller

# launch only with python3
#
#  python3 controller.py

import sys
import os
import time

sys.path.append('models')
sys.path.append('./views')

import barcode  # barcode scanner
import findObj  # findObject
from view import View
from webcam import WebCam
import imgRW
from settings import Settings
# import motion # movement 21_11_18

# chose an implementation, depending on os
if os.name == 'nt':  # sys.platform == 'win32':
	print("GPIO is not avaliable under windows!")
elif os.name == 'posix':
	print("RPI gpio init is done!")
	import gpio
else:
	raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)

Set = Settings('conf.set')
setStr = Set.load()
tmpLen = len(setStr[0]) # first setStr param is web cam res (640,480) or (640,480,15). 15 - fps. Check if camera supports it?
if tmpLen == 2:
	WebCamParam = [int(setStr[0][0]), int(setStr[0][1])] # [640, 480]
	Camera = WebCam(0, WebCamParam[0], WebCamParam[1])
elif tmpLen == 3:
	WebCamParam = [int(setStr[0][0]), int(setStr[0][1]), int(setStr[0][2])]  # 160*120 - min HD - max e.x. [640, 360, 15]
	Camera = WebCam(0, WebCamParam[0], WebCamParam[1], WebCamParam[2])

print(str(setStr[2]))
# not normal solution
if 'auto_on' in str(setStr[2]):
	autoMode = True
else:
	autoMode = False

if 'img_save_on' in str(setStr[3]):
	autoImgSave = True
else:
	autoImgSave = False

mainWindow = View("MachineImprovements", WebCamParam[0], WebCamParam[1])
ReadOrSaveImg = imgRW.ImgRW()
flag = True


# movement detection init with the equal data
# frame = Camera.takeFrame().copy() # movement 21_11_18
# MD = motion.MotionDetect(frame, frame)
# flagMovement = False
# moveTime = 0

# gpio
if os.name == 'posix':
	IO = gpio.RPI_GPIO()

# flagRobot = False
# flagTable = False
flagGPIO = False # test now
# gpio

# counter = 0
saveImgName = "Sole" # init
# machinePosArr = [0, 1]  # [0] - camera pos (robot pos - 1); [1] - robot position

soleAmmount = 0
noSoleAmmount = 0

count = 0

while mainWindow.getWindowProperty() and flag: # while True:

# gpio

	count += 1
	if os.name == 'posix':
		if IO.read() == 1:  # pos1
			if saveImgName.find("NoSole") != -1:
				# if count > 10: # needs test
				print("NoSole")
				IO.noSole()
				IO.endNoSole()

					# count = 0 # less rellay work
			elif saveImgName.find("Sole") != -1:
				# if count > 10:
				print("Sole")
				IO.sole()
				IO.endSole()

		#  make image processing simultaniouslu with robot movement

		tempIORead = IO.read()  #  for one execution IO.read for 2 cheaking
		if tempIORead == 0:  # auto or auto and table # tempIORead == 2 or tempIORead == 0
			mainWindow.simulateKeyPress(1)
# gpio

	start_time = time.time()


	frame = Camera.takeFrame().copy()
	flag = mainWindow.draw(frame) # number of pressed key

	# hide square sole pos
	if flag == 2: # ord("s") set sole pos by mouse click - crop - and unclick
		mainWindow.mousePosToZero()
		print("\'R\'" + ' ' + "Reset current square")

	# hide square sole pos
	if flag == 3 or autoMode:  # ord("d") default square (from settings file) # autoMode (auto_on) from conf.set
		mainWindow.loadDefaultSquare(frame, int(setStr[1][0]), int(setStr[1][1]), int(setStr[1][2]), int(setStr[1][3]))

		# better to make something with View draw() func
		if not autoMode: # if auto we don't need to print "Download squar..." every time
			print("\'D\'" + ' ' + "Download square pos from set file")

	if flag == 4: # save square pos (to settings)
		kok = mainWindow.returnRefPt()
		if kok != 0:
			if autoImgSave and autoMode: # for auto mod img save according conf.set
				tmpStr = "|auto_on|img_save_on"
			elif not autoImgSave and autoMode:
				tmpStr = "|auto_on|img_save_off"
			else:
				tmpStr = "|auto_off|img_save_on"

			Set.save(str(frame.shape[1]) + ',' + str(frame.shape[0]) + '|' + str(kok[0][0]) + ',' + str(kok[0][1]) + ',' +
					 str(kok[1][0]) + ',' + str(kok[1][1]) + tmpStr) # [(x1, y1), (x2, y2)])

			print("\'S\'" + ' ' + "Save square")
		else:
			print("Nothing to save!")

	# if flag == 5: # turn on/off movement detection
	# 	flagMovement = not flagMovement
	# 	print("\'M\'" + " " + str(flagMovement))
	# 	# print(chr(27) + "[2J") # clear terminal maybe in linux
	# 	os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

	# 	if 'soleImg' in locals():
	# 		MD.loadF1(soleImg)  # load zone
	# 		MD.loadF2(soleImg)  # load zone
	# 	else:
	# 		MD.loadF1(frame)  # load zone
	# 		MD.loadF2(frame)  # load zone

	# if flagMovement: #movement 21_11_18
	# 	if 'soleImg' in locals():
	# 		movementStr = MD.loadF2(soleImg)  # frame
	# 	else:
	# 		movementStr = MD.loadF2(frame)  # frame

	# 	if movementStr == -1: # not 5 iteration passed
	# 		continue
	# 	elif movementStr == 1: # movement detected
	# 		moveTime = time.time()
	# 		print("Movement! %s" % moveTime)
	# 		continue
	# 	elif movementStr == 0: # movement not detected
	# 		if (time.time() - moveTime) > 0.5:
	# 	# 		print("Ready!")
	# 			pass


	if flag == 1:  # proc only in case Space is pressed

		soleImg = mainWindow.returnSoleImg()
		cor = findObj.find(soleImg)  # sole image
		print('Processed sole res: %s %s' % (soleImg.shape[1], soleImg.shape[0]))
		isSoleStr = 'Sole(no points)'
		if not cor:
			pass
		else:
			if cor[0]/cor[1] > 0.2 and cor[1] > 8:  # and cor[0]/float(cor[1]) > 0.2: # check
				isSoleStr = 'NoSole' + '-' + str(cor[0]) + '-' + str(cor[1])
				# print(str(cor[0]) + '/' + str(cor[1]))
			else:
				isSoleStr = 'Sole'

		barCodeData = barcode.zbar(frame)

		if barCodeData is None:
			barCodeData = ['No', 'No']

		localTime = time.localtime(time.time())

		saveImgName = str(localTime[2]) + '-' + str(localTime[1]) + '-' \
					  + str(localTime[0]) + '-' + str(localTime[3]) + '-' + str(localTime[4]) + '-' \
					  + str(localTime[5]) + '-' + isSoleStr + '-' + 'QR' + '-' + str(barCodeData[1])  # 'IMGs/' +

		if autoImgSave: # auto save img according to conf
			ReadOrSaveImg.rw('W', '../IMGs/' + saveImgName + '.png', frame)  # save to img with imgName date + .png
			print('%s is saved' % saveImgName)
		else:
			print('%s' % saveImgName)
			pass

		elapsed_time = time.time() - start_time

		print("Iteration score: %f" % elapsed_time)

# free web camera and gpio in case of closing app
del IO
del Camera