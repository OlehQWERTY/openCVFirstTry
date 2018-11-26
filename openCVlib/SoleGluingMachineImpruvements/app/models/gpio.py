import RPi.GPIO as GPIO
from time import sleep  # this lets us have a time delay (see line 15)

class RPI_GPIO:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # without resistor  # input (table)
        GPIO.setup(21, GPIO.IN)  # input (robot)
        GPIO.setup(17, GPIO.OUT)  # output (table)
        GPIO.setup(18, GPIO.OUT)  # output (robot)

    def __del__(self):
        GPIO.cleanup()  # clean up after yourself

    def read(self):
        if not GPIO.input(20) and GPIO.input(21):
            # print("table + robot")
            return 0
        if not GPIO.input(20):
            # print("table")
            return 1
        if not GPIO.input(21):
            # print("robot")
            return 2
        return -1

    def sole(self):
        GPIO.output(18, 1)  # robot start
        print("Wait signal finished from robot!")
        while(self.read() != 2):
            pass
        sleep(0.5)
        GPIO.output(18, 0)  # robot stop

        GPIO.output(17, 1)  # turn table on
        print("Turn table sole")
        sleep(0.5)
        GPIO.output(17, 0)  # turn table off

    def noSole(self):
        GPIO.output(17, 1)  # turn table
        print("Wait signal finished from table!")
        while(self.read() != 1):
            pass
        sleep(0.5)
        print("Turn table NoSole")
        GPIO.output(17, 0)  # turn table