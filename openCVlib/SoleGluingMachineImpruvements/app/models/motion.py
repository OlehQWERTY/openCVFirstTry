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
            self.loadF2(self.frame2)

    def loadF1(self, frame1):
        self.frame1 = frame1.copy()
    def loadF2(self, frame2 = None):
        # if frame2 is None:
        #     frame2 = self.frame2.copy()

        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(self.prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        self.hsv[..., 0] = ang * 180 / np.pi / 2
        self.hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2BGR)

        # rgb = rgb[80:400, 20:620]  # [80:400, 20:620]
        # print(np.average(rgb))
        return np.average(rgb)
        # color mask
        # lower = [5, 1, 2]
        # lower = np.array(lower, dtype="uint8")
        # upper = [255, 255, 255]
        # upper = np.array(upper, dtype="uint8")
        #
        # mask = cv2.inRange(rgb, lower, upper)
        # output = cv2.bitwise_and(rgb, rgb, mask=mask)

        self.infinity(rgb, frame2) # output


    def infinity(self, output, frame2):
        while (1):
            cv2.imshow('frame0', self.frame1)
            cv2.imshow('frame1', output)
            cv2.imshow('frame2', frame2)  # cv2.imshow('frame2',rgb)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            elif k == ord('s'):
                cv2.imwrite('opticalfb.png', frame2)
                cv2.imwrite('opticalhsv.png', output)
            prvs = next