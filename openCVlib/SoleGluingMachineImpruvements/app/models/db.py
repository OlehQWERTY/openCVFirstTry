# sudo pip3 install cython && sudo pip3 install cymysql

# basic mySQL DB requests
# I didn't add del method for preventing errors in my app and data losing

import cymysql
import time
import sys
# from sys import exit

#!!!replace all print with log.log()!!!

sys.path.append('../models')
from debug import Debug
log = Debug(True, __name__)  # turn on/off debugging messages in this module
# log.log("Test", __name__)


class Db:
    def __init__(self, user, passwd, host, db):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.db = db
        # conn = cymysql.connect(user="monitor", passwd="password", host="localhost", db="sole_1")

    def connect(self):
        result = False
        try:
            self.conn = cymysql.connect(user=self.user, passwd=self.passwd, host=self.host, db=self.db)
        # read about possible exceptions: https://github.com/nakagami/CyMySQL/blob/master/cymysql/err.py
        except cymysql.err.MySQLError as error:
            log.log("Please check SQL server connection: " + str(error), __name__)
            # sys.exit()
        except Exception as error:  # be carefull it could grub other exception
            code, message = error.args
            log.log("Other DB error: " + str(error), __name__)
            # sys.exit()
        else:  # if no exception
            self.cur = self.conn.cursor()
            result = True
        finally:
            # pass  # perform in eny case
            return result

    def close(self):
        self.cur.close()

    def reqStandart(self):  # only for debugging
        self.cur.execute("""INSERT INTO glueMachine (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber)
            VALUES(66,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197')""")
        self.conn.commit()

    def customReq(self, string):  # "standart sql requestr"
        if self.connect():
            self.cur.execute(string)
            self.conn.commit()

    def __request(self, varUnitID, varArticul, varProcessID, varOperatorName, varPull, varOrderNumber, varLocalNumber):
        if self.connect():
            localTime = time.localtime(time.time())  # time str
            saveTime = str(localTime[2]) + '-' + str(localTime[1]) + '-' \
                       + str(localTime[0]) + '-' + str(localTime[3]) + '-' + str(localTime[4]) + '-' \
                       + str(localTime[5])

            strA = """INSERT INTO glueMachine (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber,ReadyDate) VALUES(""" \
                   + str(varUnitID) + ",\'" + str(varArticul) + "\',\'" + str(varProcessID) + "\',\'" + str(
                varOperatorName) + "\',\'" \
                   + saveTime + "\',\'" + str(varPull) + "\',\'" + str(varOrderNumber) + "\',\'" + str(
                varLocalNumber) + "\',\'" + saveTime + "\')"

            self.cur.execute(strA)
            # """INSERT INTO glueMachine (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber)
            # VALUES(66,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197')"""
            self.conn.commit()

    def req(self, varUnitID, varArticul, varProcessID, varOperatorName, varPull, varOrderNumber, varLocalNumber):
        if self.connect():
            self.__request(varUnitID, varArticul, varProcessID, varOperatorName, varPull, varOrderNumber, varLocalNumber)
            self.close()
        else:
            # can't connect
            pass

    def getAllData(self):
        if self.connect():
            self.cur.execute("SELECT * from glueMachine")
            # for r in self.cur.fetchall():  # move to getData
            #     print(r)
            self.conn.commit()  # It isn't neaded in some cases, but I don't want to get any problems because of it
            return self.cur.fetchall()

    def getData(self):  # get for instance 1 row or [column_1, column_2, column_3 ...]
        if self.connect():
            pass

    def __del__(self):
        # self.cur.close()  # don't close like this because of it can try to close not opened connection
        pass


if __name__ == '__main__':
    DB = Db("monitor", "password", "localhost", "sole_1")
    # DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')
    # DB.req()
    log.log(DB.getAllData(), __name__)