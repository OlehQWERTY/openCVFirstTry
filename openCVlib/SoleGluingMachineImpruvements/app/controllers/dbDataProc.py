#  db controller

import sys

sys.path.append('../models')

from debug import Debug
from db import Db

log = Debug(True, __name__)  # turn on/off debugging messages in this module
#
# DB = Db("monitor1", "password", "localhost", "sole_1")

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

		self.DB = Db("monitor1", "password", "localhost", "sole_1")

	def __createBunch(self, articul):
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
					self.queue.append({element: str(self.soleArtDict[element])})  # key check if here we'll get key name not value
					self.soleArtDict[element] -= 10
					# print(self.soleArtDict)

	def sendToDb(self):  # better use customReq and make other class for building request sequencies
		# write
		# add try & catch
		# take request somewhere out def ... (self, strReq)
		if self.DB.connect():
			self.DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')
			log.log(self.DbProc.getQueue(), __name__)
		else:
			log.log("Error. Can't connect to DB.", __name__)
		# del from queue data that is successfully saved to mySQL db
		pass

	# def setPath(self, path):
		# self.path = path

	def getQueue(self):
		# print(self.queue)
		return self.queue.copy()

	def delFromQueue(self, number=1):  # if queue is empty???
		for x in range(number):
			log.log(self.queue.pop(), __name__)  # "Nasty"


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

