#  db controller

import sys

sys.path.append('../models')

from debug import Debug
from db import Db

log = Debug(True, __name__)  # turn on/off debugging messages in this module

DB = Db("monitor", "password", "localhost", "sole_1")
# DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')
# DB.req()
# DB.getSelectData()

class DbDataProc():
    def __init__(self, path):
        self.soleArtDict = {}
        self.queue = []
        # self.path = path
        # self.data_new = None
        # self.data = None
        pass
    def createBunch(self, articul):
        self.soleArtDict[articul] = 0

    def addToBunch(self, articul):
        self.soleArtDict[articul] += 1

    def trySendToDb(self):
        # form list for sending to db onece in 5 minutes + save to file 1 per 20 s
    	if self.soleArtDict:  # if not empty
            for element in self.soleArtDict:
                for x in range(int(element / 10)):
                    self.soleArtDict[element] -= 10
                    self.queue.append(str(element))  # key check if here we'll get key name not value




    # def setPath(self, path):
    #     self.path = path




if __name__ == '__main__':
    print("koko")