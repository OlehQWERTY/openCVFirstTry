# sudo pip3 install cython && sudo pip3 install cymysql

import cymysql
conn = cymysql.connect(user="monitor", passwd="password", host="localhost", db="sole_1")
cur = conn.cursor()

cur.execute("""INSERT INTO glueMachine3 (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber) 
    VALUES(66,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197')""")

cur.execute("SELECT * from glueMachine3")
for r in cur.fetchall():
   # print(r[0], r[1])
   print(r)