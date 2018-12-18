#  db controller

import sys

sys.path.append('../models')

from debug import Debug
from db import Db

log = Debug(True, __name__)  # turn on/off debugging messages in this module

DB = Db("monitor1", "password", "localhost", "sole_1")

# DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')
# DB.req()
# DB.getSelectData()

del DB # close connection

class DbDataProc():
	def __init__(self, path):
		self.soleArtDict = {}
		self.queue = []
		# self.path = path
		# self.data_new = None
		# self.data = None

	def createBunch(self, articul):
		self.soleArtDict[articul] = 0

	def addToBunch(self, articul):
		self.soleArtDict[articul] += 1

	def trySendToDb(self):
		# form list for sending to db onece in 5 minutes + save to file 1 per 20 s
		if self.soleArtDict:  # if not empty
			for element in self.soleArtDict.keys():
				for x in range(int(self.soleArtDict[element] / 10)):
					self.queue.append({element:str(self.soleArtDict[element])})  # key check if here we'll get key name not value
					self.soleArtDict[element] -= 10
					# print(self.soleArtDict)

	# def setPath(self, path):
		# self.path = path

	def getQueue(self):
		# print(self.queue)
		return self.queue.copy()

	def delFromQueue(self):
		# for x in range(number):
		print(self.queue.pop())  # "Nasty"




if __name__ == '__main__':
	# print("koko")

	DbProc = DbDataProc("tempSoleDb.mdb")

	DbProc.createBunch("Nasty")

	for x in range(105):
		DbProc.addToBunch("Nasty")

	DbProc.trySendToDb()

	print(DbProc.getQueue())

	print("\n\n")

	DbProc.delFromQueue()

	print("\n\n")

	print(DbProc.getQueue())

