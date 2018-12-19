#  db controller

import sys

sys.path.append('../models')

from debug import Debug
from db import Db

log = Debug(True, __name__)  # turn on/off debugging messages in this module
#
# DB = Db("monitor", "password", "localhost", "sole_1")

# DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')
# DB.req()
# DB.getSelectData()
# del DB # close connection

class DbDataProc():
	def __init__(self, path):
		self.soleArtDict = {}
		self.queue = []
		# self.path = path
		# self.data_new = None
		# self.data = None

		self.DB = Db("monitor", "password", "localhost", "sole_1")  # you should get it somewhere out

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
				for x in range(int(self.soleArtDict[element] / 10)):
					self.queue.append({element: str(self.soleArtDict[element])})
					self.soleArtDict[element] -= 10
					# print(self.soleArtDict)

	def getQueue(self):
		# print(self.queue)
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
				self.DB.req(66, str(articul), 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')  # (66, "Nasty", ...)

				# log.log(self.DB.getAllData(), __name__)
				# print(self.DB.getAllData())
				self.showDbData(self.DB.getAllData())
		else:
			log.log("Error. Can't connect to DB.", __name__)
		# del from queue data that is successfully saved to mySQL db

	def showDbData(self, data):
		log.log("", __name__)
		for r in data:  # move to getData
			log.log(r)

	# def setPath(self, path):
		# self.path = path

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

