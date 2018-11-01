import os
pipe = os.popen('var=$(zbarimg autoImg.png | grep "QR-Code:" | tr -dc \'0-9\') | ps -face | grep zbar | awk \'{print $2}\' | xargs kill -s KILL 2> /dev/null | echo $var', 'r')
#pipe = os.popen('var=$(zbarimg autoImg.png | grep "QR-Code:" | tr -dc \'0-9\') | echo $var | ps -face | grep zbar | awk \'{print $2}\' | xargs kill -s KILL 2> /dev/null')
while True:
	a = pipe.read()
	print(a)
