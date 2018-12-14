#!/Python36/python
#Please change above path to suit your platform.  Am running it on Windows
# sudo pip3 install cython && sudo pip3 install cymysql
import MySQLdb
db = MySQLdb.connect(user="monitor",passwd="password",host="localhost",db="sole_1")
cursor = db.cursor()
cursor.execute("SELECT * from glueMachine3")
data=cursor.fetchall()
for row in data :
    print (row)
db.close()