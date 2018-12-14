# controller
# launch only with python3
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
from keys import Keys

# GPIO usage only for appropriate OS
if os.name == 'posix':
	import gpio
	IO = gpio.RPI_GPIO()
	log.log("RPI gpio init is done!", __name__)
else:
	log.log("GPIO is not avaliable for your OS!", __name__)
# settings
Set = Settings('conf.set')
setStr = Set.load()
# print(str(setStr[2]))
autoMode = True if 'auto_on' in str(setStr[2]) else False
autoImgSave = True if 'img_save_on' in str(setStr[3]) else False
# webCam
WebCamParam = [int(c) for c in setStr[0]]  # [0, 640, 480] or [0, 640, 480, 15]
Camera = WebCam(WebCamParam)  # 160*120 - min; HD - max; e.x. [0, 640, 360, 15]
# view
mainWindow = View("MachineImprovements", WebCamParam[1:3])  # WebCamParam[1] and [2]
isClosed = False
# keys
KeyA = Keys()
# findObj
ImgProc = MachineCellAnalizer()

saveImgName = "Sole"  # init
# machinePosArr = [0, 1]  # [0] - camera pos (robot pos - 1); [1] - robot position
# soleAmmount = 0
# noSoleAmmount = 0
lessRellayWorkNorm = 5
lessRellayWorkExtreme = 50
temtRellayWorkK = lessRellayWorkNorm
last_img_processing_time = time.time()
count = 0


def IO_func():  # test me
	global count, lessRellayWorkNorm, lessRellayWorkExtreme, last_img_processing_time, saveImgName
	count += 1
	if os.name == 'posix':
		# electromechanical relay lifetime optimisation
		if abs(last_img_processing_time - time.time()) > 5 * 60:  # after 20 minutes
			temtRellayWorkK = lessRellayWorkExtreme
		elif abs(last_img_processing_time - time.time()) > 0.5 * 60:  # after 5 minutes
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
		tempIORead = IO.read()  # for one execution IO.read for 2 cheaking
		if tempIORead == 0:  # auto or auto and table # tempIORead == 2 or tempIORead == 0
			mainWindow.simulateKeyPress(1)

# free web camera and gpio in case of closing app
def beforeCEnd():
	if os.name == 'posix':
		del IO
	del Camera

while mainWindow.getWindowProperty() and not isClosed:  # while True:
	IO_func()  # gpio
	frame = Camera.takeFrame().copy()
	key = mainWindow.draw(frame)  # number of pressed key
	isClosed = KeyA.keyAct(key, mainWindow, autoMode, frame, setStr, autoImgSave, Set)

	if key == 1:  # proc only in case of Space is pressed or auto mode (in auto simulates key 'space' press)
		log.log("")
		# image processing
		soleImg = mainWindow.returnSoleImg()
		saveImgName, temtRellayWorkK = ImgProc.processing(soleImg, frame, autoImgSave)

beforeCEnd()