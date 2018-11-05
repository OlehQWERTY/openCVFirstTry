import cv2

class WebCam():

    def __init__(self, camNumber=0):
        self.cam = cv2.VideoCapture(camNumber)
        for x in range(5):
            self.takeFrame()

    def takeFrame(self):
        self.ret, self.frame = self.cam.read()
        if not self.ret:
            print("Web camera isn't connected!")
            self.__del__()
        return self.frame

    def __del__(self):
        self.cam.release()
