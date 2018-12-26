import RPi.GPIO as GPIO
from time import sleep  # this lets us have a time delay (see line 15)


class RPI_GPIO:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering
        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # without resistor  # input (table in pos sign) -- #1 wire
        GPIO.setup(21, GPIO.IN)  # input (robot says table to turn)  # input (auto) -- #4 wire
        GPIO.setup(17, GPIO.OUT)  # output (table in pos sign forward to robot via RPI)  # 1001 -- # 3 wire
        GPIO.setup(18, GPIO.OUT)  # output (robot)  # i_rasp  # 1008 -- # 2 wire (if False sole else noSole - Robot)

    def __del__(self):
        GPIO.cleanup()  # clean up after yourself

    def read(self):
        if GPIO.input(20) and GPIO.input(21):
            # print("pos1 + auto")
            # test threshold protection
            sleep(0.1)  # threshold protection
            if GPIO.input(20) and GPIO.input(21):  # threshold protection
                return 0
        if GPIO.input(20):
            # print("GPIO 20 IN (pos1)")
            return 1
        if GPIO.input(21):
            # print("GPIO 21 IN (auto)")
            return 2
        return -1

    def sole(self):
        GPIO.output(18, 0)  # robot on (i_rasp)
        GPIO.output(17, 1)  # turn table on
        sleep(0.3)

    def endSole(self):
        GPIO.output(17, 0)  # turn table off
        # GPIO.output(18, 1)  # robot off

    def noSole(self):
        GPIO.output(18, 1)  # robot off (i_rasp)
        GPIO.output(17, 1)  # turn table
        sleep(0.3)

    def endNoSole(self):
        GPIO.output(17, 0)  # turn table off