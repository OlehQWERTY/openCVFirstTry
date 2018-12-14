#!/usr/bin/env python2

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "monitor", "password", "sole_1")
curs=db.cursor()

# note that I'm using triplle quotes for formatting purposes
# you can use one set of double quotes if you put the whole string on one line

# INSERT INTO glueMachine3 (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber) VALUES(0,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197');

try:
    curs.execute("""INSERT INTO glueMachine3 (UnitID,Articul,ProcessID,OperatorName,OperationDate,Pull,OrderNumber,LocalNumber) 
    VALUES(66,'Nasty',101,'Zoya Semenovna','17/11/18 17:25:36','4925NG_Poland','2564','197')""")


    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 'kitchen', 21.7)""")
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 'greenhouse', 24.5)""")
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 'garage', 18.1)""")
    #
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE(), NOW() - INTERVAL 12 HOUR, 'kitchen', 20.6)""")
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE(), NOW() - INTERVAL 12 HOUR, 'greenhouse', 17.1)""")
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE(), NOW() - INTERVAL 12 HOUR, 'garage', 16.2)""")
    #
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE(), NOW(), 'kitchen', 22.9)""")
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE(), NOW(), 'greenhouse', 25.7)""")
    # curs.execute ("""INSERT INTO tempdat
    #         values(CURRENT_DATE(), NOW(), 'garage', 18.2)""")

    db.commit()
    print("Data committed")

except:
    print("Error: the database is being rolled back")
    db.rollback()



#read data


curs.execute ("SELECT * FROM glueMachine3")

# print "\nDate     	Time		Zone		Temperature"
print("===========================================================")

for reading in curs.fetchall():
    print(str(reading[0])+"	"+str(reading[1])+" 	"+\
                reading[2]+"  	"+str(reading[3]))


print("Version: ", sys.version)