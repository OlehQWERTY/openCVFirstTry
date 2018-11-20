import RPi.GPIO as GPIO
from time import sleep  # this lets us have a time delay (see line 15)

GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering
GPIO.setup(20, GPIO.IN)  # input (table)
GPIO.setup(21, GPIO.IN)  # input (robot)
GPIO.setup(17, GPIO.OUT)  # output (table)
GPIO.setup(18, GPIO.OUT)  # output (robot)

try:
    def read(mode = 0):
        if mode == 0:
            if GPIO.input(20) and GPIO.input(21):
                print("table + robot")
                return 0
        if mode == 1:
            if GPIO.input(20):
                print("table")
                return 1
        if mode == 2:
            if GPIO.input(21):
                print("robot")
                return 2
        return -1

    def sole():
        GPIO.output(18, 1)  # robot start
        while(read(2) != 2):
            pass
        sleep(0.5)
        GPIO.output(18, 0)  # robot start

        GPIO.output(17, 1) # turn table
        sleep(0.5)
        GPIO.output(17, 0)  # turn table

    def noSole():
        GPIO.output(17, 1)  # turn table
        while (read(1) != 1):
            pass
        sleep(0.5)
        GPIO.output(17, 0)  # turn table


    # while True:  # this will carry on until you hit CTRL+C
        # print(GPIO.input(21))
        # sleep(1)
        # if GPIO.input(2): # if port 25 == 1
        #     print("LED ON")
        #     GPIO.output(17, 1)         # set port/pin value to 1/HIGH/True
        # else:
        #     print("LED OFF")
        #     GPIO.output(17, 0)         # set port/pin value to 0/LOW/False
        # sleep(0.1)         # wait 0.1 seconds

finally:  # this block will run no matter how the try block exits
    GPIO.cleanup()  # clean up after yourself