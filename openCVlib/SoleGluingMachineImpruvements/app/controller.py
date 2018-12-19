# controller
# launch only with python3
#  python3 controller.py

import sys
import os
import time

# close app in case of using pythone 2 (I have some problems with python 2 here)
if sys.version_info > (3, 0):
	pass
	# Python 3 code in this block
else:
	print("Please don't use python version less then: 3...")
	sys.exit()
	# Python 2 code in this block

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
from dbDataProc import DbDataProc

# GPIO usage only for appropriate OS
if os.name == 'posix':
	import gpio
	IO = gpio.RPI_GPIO()
	log.log("RPI gpio init is done!", __name__)
else:
	log.log("GPIO is not avaliable for your OS!", __name__)
# settings
Set = Settings('conf.set')
settings_dict = Set.load()
if settings_dict is not None:
	autoMode = settings_dict['auto']
	autoImgSave = settings_dict['imgSave']

# webCam
WebCamParam = [int(c) for c in settings_dict['cam']]  # [0, 640, 480] or [0, 640, 480, 15]
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

# DB
DbProc = DbDataProc("tempSoleDb.mdb")
DbProc.additionalData([1, 'Zoya Semenovna', '4925NG_Poland', "2564", "197"])

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
def beforeCEnd():  # (IO, Camera)
	global IO, Camera  # other way to fix: UnboundLocalError: local variable 'IO'...
	if os.name == 'posix':
		del IO
	del Camera

def QR_str_parser(saveImgName):
	if not "QR-No" in saveImgName and saveImgName.find("Sole") != -1:
		temp_a = saveImgName.find("-QR-")
		# log.log(temp_a, __name__)
		QR_str = saveImgName[(temp_a + 4):]
		# log.log(QR_str, __name__)
		return QR_str
	return None

while mainWindow.getWindowProperty() and not isClosed:  # while True:
	IO_func()  # gpio
	frame = Camera.takeFrame().copy()
	key = mainWindow.draw(frame)  # number of pressed key
	# is not checked settings_dict['soleImgPos'] existing
	isClosed = KeyA.keyAct(key, mainWindow, autoMode, frame, settings_dict['soleImgPos'], autoImgSave, Set)

	if key == 1:  # proc only in case of Space is pressed or auto mode (in auto simulates key 'space' press)
		log.log("")
		# image processing
		soleImg = mainWindow.returnSoleImg()
		saveImgName, temtRellayWorkK = ImgProc.processing(soleImg, frame, autoImgSave)

		QR_str = QR_str_parser(saveImgName)  # take QR name if Sole

		if QR_str is not None:  # better move this check inside dbDataProc???
			DbProc.addToBunch(QR_str)

		DbProc.trySendToDb()  # maybe too often???
		# save temp data to file and in 5 min send it to SQL server, if server isn't available try one more and more
		print(DbProc.getQueue())

		# make it less often
		DbProc.sendToDb()  # not finished


beforeCEnd()  # (IO, Camera) fix for: UnboundLocalError: local variable 'IO' referenced before assignment