import cv2
from time import sleep

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
        self.ret, self.frame = self.cam.read()
        if not self.ret:
            print("Web camera isn't connected!")
            self.__del__()
        return self.frame

    def __del__(self):
        self.cam.release()
