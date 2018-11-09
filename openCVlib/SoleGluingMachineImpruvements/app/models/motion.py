import cv2
import numpy as np
# cap = cv2.VideoCapture(0) # "vtest.avi"

# ret, frame1 = cap.read()
class MotionDetect:

    def __init__(self, frame1, frame2):
        if frame1 is None and frame2 is None:
            print("Error: No img!")
        else:
            self.frame1 = frame1
            self.frame2 = frame2

            self.prvs = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2GRAY)
            self.hsv = np.zeros_like(self.frame1)
            self.hsv[..., 1] = 255

            self.movementArr = [0, 0, 0, 0, 0]
            self.iterator = 0

            self.loadF2(self.frame2)
# if you need manualy compare 2 imgages so firstly
    def loadF1(self, frame1): # change first img loadF2(img), loadF1(img) and then loadF2(img2)...
        self.frame1 = frame1.copy()

    def loadF2(self, frame2 = None): # change second img
        if frame2 is None:
            frame2 = self.frame2.copy()

        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(self.prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        self.hsv[..., 0] = ang * 180 / np.pi / 2
        self.hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2BGR)

        rgb = rgb[80:400, 20:620]  # [80:400, 20:620] on the corners of img from web cam something random appears
        # print(np.average(rgb))


        # color mask
        # lower = [5, 1, 2]
        # lower = np.array(lower, dtype="uint8")
        # upper = [255, 255, 255]
        # upper = np.array(upper, dtype="uint8")
        #
        # mask = cv2.inRange(rgb, lower, upper)
        # output = cv2.bitwise_and(rgb, rgb, mask=mask)

        # self.infinity(rgb, frame2) # output debug

        imgAvarageColour = np.average(rgb)

        self.loadF1(rgb)
        return self.inertMovement(imgAvarageColour) # inert

    def inertMovement(self, imgAvarageColour):
        # print(self.iterator)
        self.movementArr[self.iterator] = imgAvarageColour
        self.iterator = self.iterator + 1
        if self.iterator >= 5:
            self.iterator = 0
            extremeMov = max(self.movementArr) - sum(self.movementArr)/5
            # print(max(self.movementArr))
            # self.movementArr = np.linspace(self.movementArr)
            if extremeMov > 1: # max - average                       # sensetivity !!!!!!!!!!!!!!!!!!!
                return 1 #"Movement detected!"
            else:
                return 0 #"No movement"
        return -1 # not fiveth call

