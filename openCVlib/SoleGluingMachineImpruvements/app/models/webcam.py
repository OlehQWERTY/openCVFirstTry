import cv2
from time import sleep
import os

class WebCam():
    def __init__(self, WebCamParam = [0, 640, 480, 15]):  # [cam_number = 0, w = 640, h = 480, fps = 15]
        print(WebCamParam)
        self.cam = cv2.VideoCapture(WebCamParam[0])
        self.cam.set(3, WebCamParam[1])  # w
        self.cam.set(4, WebCamParam[2])  # h
        if len(WebCamParam) > 3:
            self.cam.set(WebCamParam[3], 0.1)  # fps
        for x in range(5):
            sleep(0.1)
            self.takeFrame()

    def takeFrame(self):
        self.ret, self.frame = self.cam.read()

        if not self.ret:
            print("Error: Web camera isn't connected or busy!\nPlease, try to reboot RPI.")
            # rewrite this part a little - try connect one more

            self.del_reboot()
            exit()  # try exec(this python script)

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