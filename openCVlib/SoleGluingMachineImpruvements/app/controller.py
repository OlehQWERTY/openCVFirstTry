# controller
# launch only with python3
# python3 controller.py

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
from settings import Settings as S  # import as S (shorter name)
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
def loadSettings(Set):
	global settings_dict, autoMode, autoImgSave, autoImgQR
	settings_dict = Set.load()
	if settings_dict is not None:
		autoMode = settings_dict['auto']
		autoImgSave = settings_dict['imgSave']
		autoImgQR = settings_dict['autoImgQR']

		if autoImgQR:
			log.log("Avoid usage autoImgQR on real machine because it's possible to lose \"auto\" robot signal!", __name__)

Set = S('conf.set')
loadSettings(Set)

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
lessRellayWorkNorm = 5  # 5
lessRellayWorkExtreme = 50  # 50
temtRellayWorkK = lessRellayWorkNorm
last_img_processing_time = time.time()
count = 0
io_img_proc_falag = False  # test
prevSaveImgName = "Sole"

# DB
DbProc = DbDataProc("dbQueue.mdb")
DbProc.additionalData([1, 'Zoya Semenovna', '4925NG_Poland', "2564", "197"])
last_sending_to_db = time.time()
last_trying_to_sending_to_db = time.time()
lessSendToDB = 5*60  # send less then once per X seconds
lessTryToSendToDB = 5  # store locally less then once per X seconds

# temp
barcodePos = None  # it is neaded by barcodeSquareDraw out of if key == 1:
lastQRDetection = None
# temp

def IO_func():
	global count, lessRellayWorkNorm, lessRellayWorkExtreme, last_img_processing_time, saveImgName
	global io_img_proc_falag  # test
	count += 1
	if os.name == 'posix':  # too often

		if IO.read() == 1:  # pos1
			# electromechanical relay lifetime optimisation
			if abs(last_img_processing_time - time.time()) > 5 * 60:  # after 20 minutes
				temtRellayWorkK = lessRellayWorkExtreme
			elif abs(last_img_processing_time - time.time()) > 0.5 * 60:  # after 5 minutes
				temtRellayWorkK = lessRellayWorkExtreme / 5
			else:
				temtRellayWorkK = lessRellayWorkNorm

			# if saveImgName.find("NoSole") != -1:
			if prevSaveImgName.find("NoSole") != -1:
				if count > temtRellayWorkK:  # if count > 5:
					log.log("NoSole", __name__)
					IO.noSole()
					IO.endNoSole()
					count = 0  # 1 less rellay work
			# elif saveImgName.find("Sole") != -1:
			elif prevSaveImgName.find("Sole") != -1:
				if count > temtRellayWorkK:  # if count > 5:
					log.log("Sole", __name__)
					IO.sole()
					IO.endSole()
					count = 0  # 1 less relay work

			# print("temtRellayWorkK", temtRellayWorkK)

		#  make image processing simultaneously with robot movement
		# tempIORead = IO.read()  # for one execution IO.read for 2 cheaking
		# if tempIORead == 0:  # auto or auto and table # tempIORead == 2 or tempIORead == 0
		# 	mainWindow.simulateKeyPress(1)

		tempIORead = IO.read()  # for one execution IO.read for 2 cheaking
		if tempIORead == 3 and not io_img_proc_falag:  # work and table
			mainWindow.simulateKeyPress(1)
			io_img_proc_falag = True
			# time.sleep(1)  # can't detect qr solution (rest table movement)
		elif tempIORead == 0:  # auto and table # tempIORead == 2 or tempIORead == 0
			io_img_proc_falag = False


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

# def QR_str_parser(prevSaveImgName):
# 	if not "QR-No" in prevSaveImgName and prevSaveImgName.find("Sole") != -1:
# 		temp_a = prevSaveImgName.find("-QR-")
# 		# log.log(temp_a, __name__)
# 		QR_str = prevSaveImgName[(temp_a + 4):]
# 		# log.log(QR_str, __name__)
# 		return QR_str
# 	return None

def barcodeSquareDraw(barcodePos, mainWindow):
	global lastQRDetection  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!1
	# temp
	if barcodePos:  # it is neaded by barcodeSquareDraw out of if key == 1:
	# temp
		if barcodePos is not None:
			# log.log(barcodePos, __name__)
			# move it to other place
			temp_list = [((barcodePos['x'], barcodePos['y']), (barcodePos['w'], barcodePos['h'])), (255, 0, 0)]
			# print(temp_list)
			mainWindow.clearRectList()  # clear old rectangles
			mainWindow.rectStoreList(temp_list)  # add new qt rectangle

			# temp
			lastQRDetection = time.time()


while mainWindow.getWindowProperty() and not isClosed:  # while True:
	IO_func()  # gpio
	frame = Camera.takeFrame().copy()
	key = mainWindow.draw(frame)  # number of pressed key
	# is not checked settings_dict['soleImgPos'] existing
	isClosed = KeyA.keyAct(key, mainWindow, autoMode, frame, settings_dict['soleImgPos'], autoImgSave, autoImgQR, Set)

	if KeyA.needReloadSettings():  # automode and autoImgSave key change need it (find answers in keys.py)
		loadSettings(Set)
		KeyA.reloagFlagSetFalse()

	# time_test1 = time.time()
	if autoImgQR and count >= lessRellayWorkNorm - 1:  # auto barcode pos
		barCodeData, barcodePos = ImgProc.barcodeProcessing(frame)
		barcodeSquareDraw(barcodePos, mainWindow)
	# time_test2 = time.time() - time_test1
	# if time_test2 > 0.3:
	# 	print("QR time", time_test2)

	# fix it repitedly clearRectList()
	if lastQRDetection and abs(lastQRDetection - time.time()) > 3:  # hide QR code square in 1s
		mainWindow.clearRectList()

	if key == 1:  # proc only in case of Space is pressed or auto mode (in auto simulates key 'space' press)
		prevSaveImgName = saveImgName  # prevPos is processed (machine where cam -1 pos); for -2 pos prevprev -> prev -> now
		log.log("")
		# image processing
		last_img_processing_time = time.time()  # we needs it for relay life time extention
		soleImg = mainWindow.returnSoleImg()
		frame = Camera.takeFrame().copy()  # test
		saveImgName, temtRellayWorkK, barcodePos = ImgProc.processing(soleImg, frame, autoImgSave)

		barcodeSquareDraw(barcodePos, mainWindow)  # barcode square show on the main window

		QR_str = QR_str_parser(saveImgName)  # take QR name if Sole

		if QR_str is not None:  # better move this check inside dbDataProc??? guess no! more independence
			DbProc.addToBunch(QR_str)
			log.log("QR Code: " + QR_str, __name__)  # debug only
		else:
			DbProc.addToBunch("unknown")  # if QR code not detected
			log.log("QR Code: unknown", __name__)  # debug only

		# dbDataProc
		temp_Time = time.time()
		# no need abs(), but who knows :)
		if abs(temp_Time - last_sending_to_db) > lessSendToDB:
			# make it less often
			DbProc.sendToDb()  # not finished
			print("lessSendToDB")
			last_sending_to_db = time.time()
		elif abs(temp_Time - last_trying_to_sending_to_db) > lessTryToSendToDB:  # not oftener than once per 4 s
			DbProc.trySendToDb()  # maybe too often???
			# save temp data to file and in 5 min send it to SQL server, if server isn't available try one more and more
			# print(DbProc.getQueue())
			print("lessTryToSendToDB")
			last_trying_to_sending_to_db = time.time()

beforeCEnd()  # (IO, Camera) fix for: UnboundLocalError: local variable 'IO' referenced before assignment