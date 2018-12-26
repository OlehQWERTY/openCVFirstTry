#  db controller

import sys

sys.path.append('../models')

from debug import Debug
from db import Db

log = Debug(True, __name__)  # turn on/off debugging messages in this module
#
# DB = Db("monitor", "password", "localhost", "sole_1")

# DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197', 27)
# DB.req()
# DB.getSelectData()
# del DB # close connection

class DbDataProc():
	def __init__(self, path):
		self.soleArtDict = {}
		self.queue = []
		self.setPath(path)  # func is used to make possible changing file path on the run

		self.DB = Db("monitor", "password", "localhost", "sole_1")  # you should get it somewhere out
		self.machinePreset = None  # machine file (preset for current machine) (set from other PC)

	def __createBunch(self, articul):  # add other fields for db (UnitID,Articul,ProcessID,OperatorName,OperationDate ...)
		# mod: key - articull ?, val = [?, ?, ?]
		self.soleArtDict[articul] = 0


	def addToBunch(self, articul):
		if articul in self.soleArtDict.keys():
			self.soleArtDict[articul] += 1
		else:
			self.__createBunch(articul)
			log.log("Unknown article. New bunch is created: ", __name__)

	def trySendToDb(self):
		# form list for sending to db onece in 5 minutes + save to file 1 per 20 s
		if self.soleArtDict:  # if not empty
			for element in self.soleArtDict.keys():
				for x in range(int(self.soleArtDict[element] / 4)):  # 10 pairs of sole 10 * 2 = 20 (Left + Right)
					self.queue.append({element: str(self.soleArtDict[element])})  # add other fields ()
					self.soleArtDict[element] -= 4
					# print(self.soleArtDict)

	def getQueue(self):
		# print(self.queue)
		# for x in self.queue:
		# 	log.log(x)
		return self.queue.copy()

	def sendToDb(self):  # better use customReq and make other class for building request sequencies
		# write
		# add try & catch
		# take request somewhere out def ... (self, strReq)
		if self.DB.connect():
			tempArticul = self.delFromQueue()
			if tempArticul:  # self.queue is not empty
				# print("----------", list(tempArticul.keys())[0])  # .keys() - not a list, it is View so we convert it

				articul = list(tempArticul.keys())[0]
				if self.machinePreset:  # if machine preset is specified
					self.DB.req(str(self.machinePreset[0]), str(articul), 101, str(self.machinePreset[1]), str(self.machinePreset[2]), \
								str(self.machinePreset[3]), str(self.machinePreset[4]))  # (66, "Nasty", ...)

				# log.log(self.DB.getAllData(), __name__)
				# print(self.DB.getAllData())
				self.showDbData(self.DB.getAllData())
		else:
			log.log("Error. Can't connect to DB.", __name__)
		# del from queue data that is successfully saved to mySQL db

	def additionalData(self, machine=None):
		# UnitID, Articul, OperatorName, OperationDate
		# ProcessID 101 add
		# ProcessID 102 remove (send somewhere)
		# ProcessID 103 remove Error
		# ProcessID 104 remove fault in the design
		# varUnitID, varArticul, varProcessID, varOperatorName, varPull, varOrderNumber, varLocalNumber

		# self.machine = [1, 'Zoya Semenovna', '4925NG_Poland', "2564", "197"]  # only for test here
		if not machine:
			log.log("Machine not specified", __name__)
			# don't do anything with bd...
			return None
		else:
			self.machinePreset = machine.copy()

	def showDbData(self, data):
		log.log("", __name__)
		for r in data:  # move to getData
			log.log(r)

	# def wrap for db countArticulSize
	def getColumn(self, columnName, rowName = None):  # way to use DB.getColumnContent(columnName, rowName) here
		return self.DB.getColumnContent(columnName, rowName)

	def setPath(self, path=None):  # no need to use this
		self.path = path

	def showPath(self, path = None):  # no need to use this
		if path:
			log.log(self.path, __name__)

	def delFromQueue(self, number=1):  # if queue is empty???
		if self.queue:  # not empty list
			for x in range(number):
				print(self.queue)
				lastElement = self.queue.pop()
				log.log("delFromQue: ", __name__)
				log.log(lastElement, __name__)  # "Nasty"
				return lastElement  # return del element
		else:
			log.log("delFromQue: queue is empty!", __name__)
			return None


if __name__ == '__main__':
	DbProc = DbDataProc("tempSoleDb.mdb")

	for x in range(105):
		DbProc.addToBunch("Nasty")
	for x in range(80):
		DbProc.addToBunch("Katy")

	DbProc.trySendToDb()
	print(DbProc.getQueue())
	print("\n\n")
	DbProc.delFromQueue()
	print("\n\n")
	print(DbProc.getQueue())
	DbProc.sendToDb()
	print("\n\n")
	print(DbProc.getQueue())

	print(DbProc.getColumn("Articul"))

