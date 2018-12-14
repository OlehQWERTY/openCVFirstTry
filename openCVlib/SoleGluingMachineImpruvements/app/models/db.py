# sudo pip3 install cython && sudo pip3 install cymysql

import cymysql
import time


class Db:
    def __init__(self, user, passwd, host, db):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.db = db

        # conn = cymysql.connect(user="monitor", passwd="password", host="localhost", db="sole_1")
        self.conn = cymysql.connect(user=self.user, passwd=self.passwd, host=self.host, db=self.db)
        self.cur = self.conn.cursor()

    def reqStandart(self):
        self.cur.execute("""INSERT INTO glueMachine3 (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber)
            VALUES(66,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197')""")
        self.conn.commit()

    def simpleReq(self, string):
        self.cur.execute(string)

    def req(self, varUnitID, varArticul, varProcessID, varOperatorName, varPull, varOrderNumber, varLocalNumber):
        localTime = time.localtime(time.time())  # time str
        saveTime = str(localTime[2]) + '-' + str(localTime[1]) + '-' \
                   + str(localTime[0]) + '-' + str(localTime[3]) + '-' + str(localTime[4]) + '-' \
                   + str(localTime[5])

        strA = """INSERT INTO glueMachine3 (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber) VALUES(""" \
               + str(varUnitID) + ",\'" + str(varArticul) + "\',\'" + str(varProcessID) + "\',\'" + str(
            varOperatorName) + "\',\'" \
               + saveTime + "\',\'" + str(varPull) + "\',\'" + str(varOrderNumber) + "\',\'" + str(
            varLocalNumber) + "\')"

        # print(strA)

        self.cur.execute(strA)
        # """INSERT INTO glueMachine3 (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber)
        # VALUES(66,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197')"""
        # self.conn.commit()

    def getSelectData(self):
        self.cur.execute("SELECT * from glueMachine3")
        for r in self.cur.fetchall():
            # print(r[0], r[1])
            print(r)
        # self.conn.commit()  # It isn't neaded in some cases, but I don't want to get any problems because of it

    def __del__(self):
        self.cur.close()


if __name__ == '__main__':
    DB = Db("monitor", "password", "localhost", "sole_1")
    DB.req(66, 'Nasty', 101, 'Zoya Semenovna', '4925NG_Poland', '2564', '197')
    # DB.req()
    DB.getSelectData()