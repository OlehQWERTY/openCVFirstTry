import cv2
from time import sleep
import os

class WebCam():
    def __init__(self, camNumber=0, w = 640, h = 480, fps = 15):
        self.cam = cv2.VideoCapture(camNumber)
        self.cam.set(3, w) # w
        self.cam.set(4, h)
        self.cam.set(fps, 0.1)
        for x in range(5):
            sleep(0.1)
            self.takeFrame()

    def takeFrame(self):
        # check if this is normally work
        # for i in range(3):  # trying to escape bed image of ghost image (looks like prev image covers current)
        self.ret, self.frame = self.cam.read()

        if not self.ret:
            print("Error: Web camera isn't connected or busy!\nPlease, try to reboot RPI.")
            # rewrite this part a little - try connect one more

            self.del_reboot()
            exit()

        return self.frame

    def __del__(self):
        self.cam.release()

    def del_reboot(self):
        print("Autoreboot RPI in 5 s...")
        for i in range(10):  # not tested
            sleep(0.5)
            print(i/2) if i%2 == 0 else False

        self.cam.release()
        os.popen('reboot')  # find better approach