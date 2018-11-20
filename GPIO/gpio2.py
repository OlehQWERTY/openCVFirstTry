import RPi.GPIO as GPIO  
from time import sleep     # this lets us have a time delay (see line 15)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(21, GPIO.IN)    # set GPIO25 as input (button)  
GPIO.setup(17, GPIO.OUT)   # set GPIO24 as an output (LED)  
  
try:  
    while True:            # this will carry on until you hit CTRL+C  
    	print(GPIO.input(21))
    	sleep(1)
        # if GPIO.input(2): # if port 25 == 1  
        #     print("LED ON")
        #     GPIO.output(17, 1)         # set port/pin value to 1/HIGH/True  
        # else:  
        #     print("LED OFF")
        #     GPIO.output(17, 0)         # set port/pin value to 0/LOW/False  
        # sleep(0.1)         # wait 0.1 seconds  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  