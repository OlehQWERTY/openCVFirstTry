import RPi.GPIO as GPIO
from time import sleep  # this lets us have a time delay (see line 15)

class RPI_GPIO:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # without resistor  # input (table) -- #1 wire
        GPIO.setup(21, GPIO.IN)  # input (robot)  # input (auto) -- #4 wire
        GPIO.setup(17, GPIO.OUT)  # output (table)  # 1001 -- # 3 wire
        GPIO.setup(18, GPIO.OUT)  # output (robot)  # i_rasp  # 1008 -- # 2 wire

    def __del__(self):
        GPIO.cleanup()  # clean up after yourself

    def read(self):
        if GPIO.input(20) and GPIO.input(21):
            # print("table + robot")
            return 0
        if GPIO.input(20):
            # print("table")
            return 1
        if GPIO.input(21):
            # print("robot")
            return 2
        return -1

    def sole(self):
        # GPIO.output(18, 1)  # robot start
        # print("Wait signal finished from robot!")
        # while(self.read() != 2):
        #     pass
        # sleep(0.5)
        GPIO.output(18, 0)  # robot on
        GPIO.output(17, 1)  # turn table on
        sleep(2)
        

    def endSole(self):

        # sleep(1)

        print("Turn table sole")
        # sleep(0.5)
        GPIO.output(17, 0)  # turn table off

        GPIO.output(18, 1)  # table off
        # sleep(2)
        

    def noSole(self):
        GPIO.output(18, 1)  # turn table off
        GPIO.output(17, 1)  # turn table
        # print("Wait signal finished from table!")
        # while(self.read() != 1):
        #     pass
        sleep(2)


    def endNoSole(self):
        sleep(1)
        print("Turn table NoSole")
        GPIO.output(17, 0)  # turn table off
        # sleep(2)