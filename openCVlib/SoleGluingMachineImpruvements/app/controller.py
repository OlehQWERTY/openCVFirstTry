# controller

# launch only with python3
#
#  python3 controller.py

import sys
import os
import time

sys.path.append('models')
sys.path.append('./views')
sys.path.append('controllers')

from debug import Debug
log = Debug(True, __name__)  # turn on/off debugging messages in this module
from view import View
from webcam import WebCam
from settings import Settings
from machineCellAnalizer import MachineCellAnalizer


# chose an implementation, depending on os
if os.name == 'nt':  # sys.platform == 'win32':
	log.log("GPIO is not avaliable under windows!", __name__)
elif os.name == 'posix':
	log.log("RPI gpio init is done!", __name__)
	import gpio
else:
	raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)

Set = Settings('conf.set')
setStr = Set.load()
tmpLen = len(setStr[0]) # first setStr param is web cam res (640,480) or (640,480,15). 15 - fps. Check if camera supports it?
if tmpLen == 2:
	WebCamParam = [int(setStr[0][0]), int(setStr[0][1])]  # [640, 480]
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

flag = True

# gpio
if os.name == 'posix':
	IO = gpio.RPI_GPIO()
# gpio

# counter = 0
saveImgName = "Sole"  # init
# machinePosArr = [0, 1]  # [0] - camera pos (robot pos - 1); [1] - robot position

soleAmmount = 0
noSoleAmmount = 0
lessRellayWorkNorm = 5
lessRellayWorkExtreme = 50
temtRellayWorkK = lessRellayWorkNorm
last_img_processing_time = time.time()

count = 0

ImgProc = MachineCellAnalizer()  # 11111111111111111111111111111111111111

while mainWindow.getWindowProperty() and flag:  # while True:

# gpio

	count += 1
	if os.name == 'posix':

		# electromechanical relay lifetime optimisation
		if abs(last_img_processing_time - time.time()) > 5*60:  # after 20 minutes
			temtRellayWorkK = lessRellayWorkExtreme
		elif abs(last_img_processing_time - time.time()) > 0.5*60:  # after 5 minutes
			temtRellayWorkK = lessRellayWorkExtreme / 5
		else:
			temtRellayWorkK = lessRellayWorkNorm


		if IO.read() == 1:  # pos1
			if saveImgName.find("NoSole") != -1:
				if count > temtRellayWorkK:  # if count > 5:
					log.log("NoSole", __name__)
					IO.noSole()
					IO.endNoSole()
					count = 0  # 1 less rellay work

			elif saveImgName.find("Sole") != -1:
				if count > temtRellayWorkK:  # if count > 5:
					log.log("Sole", __name__)
					IO.sole()
					IO.endSole()
					count = 0  # 1 less relay work

		#  make image processing simultaneously with robot movement

		tempIORead = IO.read()  #  for one execution IO.read for 2 cheaking
		if tempIORead == 0:  # auto or auto and table # tempIORead == 2 or tempIORead == 0
			mainWindow.simulateKeyPress(1)
# gpio

	frame = Camera.takeFrame().copy()
	flag = mainWindow.draw(frame)  # number of pressed key

	# save highlighted square as sole pos
	if flag == 2:  # ord("s") set sole pos by mouse click - crop - and unclick
		mainWindow.mousePosToZero()
		log.log("\'R\'" + ' ' + "Reset current square", __name__)

	# hide square sole pos
	if flag == 3 or autoMode:  # ord("d") default square (from settings file) # autoMode (auto_on) from conf.set
		mainWindow.loadDefaultSquare(frame, int(setStr[1][0]), int(setStr[1][1]), int(setStr[1][2]), int(setStr[1][3]))

		# better to make something with View draw() func
		if not autoMode:  # if auto we don't need to print "Download squar..." every time
			log.log("\'D\'" + ' ' + "Download square pos from set file", __name__)

	if flag == 4:  # save square pos (to settings)
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


	if flag == 1:  # proc only in case Space is pressed or auto mode
		log.log("")
		# image processing
		soleImg = mainWindow.returnSoleImg()
		saveImgName, temtRellayWorkK = ImgProc.processing(soleImg, frame, autoImgSave)

# free web camera and gpio in case of closing app
if os.name == 'posix':
	del IO

del Camera