import cv2
import math # sqrt()

class View:

    def __init__(self, name, w = 640, h = 480): # w h are neaded for texting resolution
        if name is None:
            print("Can't create window without name!")
        else:
            self.name = name
            cv2.namedWindow(self.name)
            self.createTrackbar('resMode', int(math.sqrt(w/80))) # 640 * 480 shows 2 against 3
            self.setCamW = w # change
            self.setCamH = h
            # self.ResModeVal = 3 # 640 * 480
            # self.ResMode()
        # self.max = max

    def nothing(self, val):
        print("nothing")
        pass

    def resMode(self, val):
        # print("camRes")
        self.setCamW = pow(2, val) * 80  # ... 1 - 160*120 2 - 320*240 3 - 640*480 4 - 1280*720

        if self.setCamW == 1280: # other screen ratio (16*9)
            self.setCamH = 720
        else:
            self.setCamH = int(self.setCamW * 3 / 4) # screen ratio (4*3)
        # pass

    def createTrackbar(self, name = 'resMode', val=0, maxVal = 4):
        # if name is 'camResolution':
        #     # print('Trackbar \'camResolution\' already exist!')
        #     pass
        # else:
        # print('pek pek pek')
        # if 'self.trackbarName' in locals():
        #     if self.trackbarName is 'camResolution':
        #         pass
        #     else:
        #         self.trackbarName = name
        #         self.trackbarVal = val
        #         self.trackbarMaxVal = maxVal

        if name is 'resMode':
            self.trackbarName = name # temp crutch
            self.trackbarVal = val
            # if 'self.trackbarName' in globals(): #locals()
            # self.resModeVal = self.getTrackbarPos(self.trackbarName, self.name)
            # self.trackbarVal = self.resModeVal #.getTrackbarPos(self.trackbarName, self.name)  # trackbar read position
            # print(self.trackbarVal)
            # else:
            #     self.trackbarVal = val
            self.trackbarMaxVal = maxVal
            cv2.createTrackbar(self.trackbarName, self.name, self.trackbarVal, self.trackbarMaxVal, self.resMode) # trackbar
        # else:
        #     # self.trackbarName = name  # temp crutch
        #     cv2.createTrackbar(self.trackbarName, self.name, self.trackbarVal, self.trackbarMaxVal, self.nothing)  # trackbar
        # # cv2.createTrackbar(self.trackbarName, self.name, 3, self.trackbarVal, self.nothing)
        # # resW = cv2.getTrackbarPos('camResolution', 'test_cam')  # trackbar read position

    def show(self, img):
        # width = int(frame.shape[1] * percent / 100)
        # height = int(frame.shape[0] * percent / 100)
        cv2.resizeWindow(self.name, img.shape[1], img.shape[0]) # resize window according to web camera frame resolution
        cv2.putText(img, 'proc: ' + str(self.setCamW) + '*' + str(self.setCamH), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255, 255, 0), 2)
        cv2.putText(img, 'orig: ' + str(img.shape[1]) + '*' + str(img.shape[0]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 0), 2)
        cv2.imshow(self.name, img)
        # if self.name is 'MachineImprovements': # not universal approach (MachineImprovements should be first window)
        # cv2.putText(img, str(self.setCamW) + '*' + str(self.setCamH), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        #             (255, 255, 0), 2)
        # self.createTrackbar('resMode')
        self.k = cv2.waitKey(1)  # 50 # don't work without this
        return self.key()

    # def resize(self, img):
    #     imgToShow = cv2.resize(img, (self.setCamW, self.setCamH))

    def key(self): # pressed key proc
        # print(self.k)
        if self.k == 27: # ESC
            return 0
        elif self.k == 32: # Space
            return 1
        else:
            return 100

    def moveWindow(self, x, y):
        cv2.moveWindow(self.name, x, y)

    def getWindowProperty(self):
        if cv2.getWindowProperty(self.name, 0) >= 0: # this will send True if !(X window button) when the current window will be closed
            return True
        else:
            return False

    def __del__(self):
        if self.name is None:
            pass
        else:
            cv2.destroyWindow(self.name)
