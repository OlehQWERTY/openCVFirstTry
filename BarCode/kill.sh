 #kill all running zbar tasks ... call from python 
ps -face | grep zbar | awk '{print $2}' | xargs kill -s KILL