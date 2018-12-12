# It is needed to divide this class to two files: view controller + universal view for any purposes
# create #1 view - main window #2 view - first additional window ...
# add callback for spec view func (additional windows needs to drow something spec so just make draw(callback) in basic obj)

import cv2
import math # sqrt()
import os # auto change os type


class View:

    def __init__(self, name, w = 640, h = 480): # w h are neaded for texting resolution
        if name is None:
            print("Can't create window without name!")
        else:
            self.name = name
            cv2.namedWindow(self.name)
            if w == 640:
                # in case of vga resolution return 2 val (the same as 320*240)
                self.createTrackbar('resMode', int(math.sqrt(w/80))+1) # 640 * 480 shows 2 instead of 3
            else:
                self.createTrackbar('resMode', int(math.sqrt(w / 80)))  # 640 * 480 shows 2 instead of 3

            self.setCamW = w # change
            self.setCamH = h

            cv2.setMouseCallback(self.name, self.click_and_crop) # mouse callback

            self.mousePos = None

            self.flg1 = True # crutch

            self.flg2 = False # close sole window

            self.simulatedKey = -1 # simulate Key var


    def click_and_crop(self, event = None, x = None, y = None, flags = None, param = None): # def click_and_crop(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False
            self.mousePos = self.refPt  # crutch

        elif event == cv2.EVENT_MOUSEMOVE: # movement pos
            self.mouseMovementPos = (x, y)
        #     pass

            # print(x, y)

            # draw a rectangle around the region of interest
            # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            # cv2.imshow("image", image)

    def returnRefPt(self): # crutch for refPt available from outside
        if self.mousePos is None:
            return 0
        else:
            if len(self.mousePos) == 2:
                return self.mousePos
            else:
                return 0

    def nothing(self, val): # for events if we don't need to do anything
        print("nothing")
        pass

    def resMode(self, val):
        self.setCamW = pow(2, val) * 80  # ... 1 - 160*120 2 - 320*240 3 - 640*480 4 - 1280*720
        if self.setCamW == 1280: # other screen ratio (16*9)
            self.setCamH = 720
        else:
            self.setCamH = int(self.setCamW * 3 / 4) # screen ratio (4*3)

    def createTrackbar(self, name = 'resMode', val=0, maxVal = 4): # make it universal for enu window
        if name is 'resMode':
            self.trackbarName = name # temp crutch
            self.trackbarVal = val
            self.trackbarMaxVal = maxVal
            cv2.createTrackbar(self.trackbarName, self.name, self.trackbarVal, self.trackbarMaxVal, self.resMode) # trackbar

    def simulateKeyPress(self, key=-1):
        if key != -1:
            self.simulatedKey = key
            return key
        return -1

    def draw(self, img):
        self.show2(img)

        self.show1(img) # temp order
        self.k = cv2.waitKey(1)  # 50 # don't work without this

        # print(self.simulatedKey)

        if self.simulatedKey != -1:  # simulate key pres from program
            tmpKey = self.simulatedKey
            self.simulatedKey = -1
            return tmpKey

        return self.key()  # return pressed key (ESC - exit)


    def show1(self, img): # mainWindow
        cv2.resizeWindow(self.name, img.shape[1],
                         img.shape[0])  # resize window according to web camera frame resolution
        # where width - frame.shape[1], height - frame.shape[0]
        cv2.putText(img, 'proc: ' + str(self.setCamW) + '*' + str(self.setCamH), (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0), 2)
        cv2.putText(img, 'orig: ' + str(img.shape[1]) + '*' + str(img.shape[0]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0), 2)
        cv2.imshow(self.name, img)

    def show2(self, img):  # addition window with squared part of main window
        # square according to mouse
        if self.flg1:  # crutch
            self.mousePos1 = self.returnRefPt()
        if self.mousePos1 != 0:

            x1 = self.mousePos1[0][0]
            x2 = self.mousePos1[1][0]

            y1 = self.mousePos1[0][1]  # (x y)
            y2 = self.mousePos1[1][1]
            # imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            if (x1 < x2) and (y1 < y2): # 5 options x1 < x2 and y1 > y2 .... are neaded
                if x2 - x1 < 50: # min size
                    x2 = (int(x1/50) + 1) * 50
                    print(x2)
                if y2 - y1 < 50:
                    y2 = (int(y1/50) + 1) * 50
                    print(y2)
                self.soleImg = img[y1:y2, x1:x2]  # +1 because program crashes in case of 0 size
            elif x1 == x2 and y1 == y2:
                x2 = x1 + 50
                y2 = y1 + 50
                self.soleImg = img[y1:y2, x1:x2]  # +1 because program crashes in case of 0 size
            else:
                if x1 - x2 < 50: # min size
                    x1 = (int(x2/50) + 1) * 50
                    print(x1)
                if y1 - y2 < 50:
                    y1 = (int(y2/50) + 1) * 50
                    print(y1)
                self.soleImg = img[y2:y1, x2:x1]
            # test auto change os V (line below doesn't work in RPI) ***** TEST
            cv2.namedWindow('SoleImg', 0 if os.name == 'nt' else 1)  # resize window in another way !!!!!! try cv2.GUI_EXPANDEDS cv2.WINDOW_GUI_NORMAL
            cv2.resizeWindow("SoleImg", self.soleImg.shape[1],
                             self.soleImg.shape[0])  # resize window according to web camera frame resolution

            cv2.imshow("SoleImg", self.soleImg)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2) # ????



    def loadDefaultSquare(self, img, x1 = 0, y1 = 0, x2 = 1, y2 = 1): # crutch
        self.mousePos1 = [(x1, y1), (x2, y2)]

        self.soleImg = img[self.mousePos1[0][1]:self.mousePos1[1][1] + 1,
                       self.mousePos1[0][0]:self.mousePos1[1][0] + 1]  # +1 because program crashes in case of 0 size
        cv2.resizeWindow("SoleImg", self.soleImg.shape[1],
                         self.soleImg.shape[0])  # resize window according to web camera frame resolution
        cv2.namedWindow('SoleImg', 0 if os.name == 'nt' else 1)  # resize window in another way !!!!!! try cv2.GUI_EXPANDEDS cv2.WINDOW_GUI_NORMAL
        cv2.imshow("SoleImg", self.soleImg)
        cv2.rectangle(img, (self.mousePos1[0][0], self.mousePos1[0][1]), (self.mousePos1[1][0] + 1, self.mousePos1[1][1] + 1),
                      (0, 0, 255), 2)

    def returnSoleImg(self):  # crutch
        return self.soleImg

    def resizeImg(self, img, w=0, h=0):
        if w!=0 and h!=0 and w > 0 and h > 0:
            img = cv2.resize(img, (w, h))
        else:
            img = cv2.resize(img, (self.setCamW, self.setCamH))
        return img.copy()

    def key(self):  # pressed key proc
        # print(self.k)
        if self.k == 27:  # ESC
            return 0
        elif self.k == 32:  # Space
            return 1
        # if the 'r' key is pressed, break from the loop
        elif self.k == ord("r"):  # del sole position on the screen
            return 2
        elif self.k == ord("d"):  # default square (from settings)
            self.flg1 = not self.flg1  # crutch
            return 3
        elif self.k == ord("s"):  # save square pos (to settings)
            self.flg1 = not self.flg1  # crutch
            return 4
        else:
            return 100

    def moveWindow(self, x, y):  # set window pos (not used now)
        cv2.moveWindow(self.name, x, y)

    def mousePosToZero(self):  # this func is responsible for hiding square (mouse pressed and unpressed pos)
        self.mousePos = None
        cv2.destroyWindow("SoleImg")  # move it somewhere else

    def getWindowProperty(self): # used for closing program by pressing exit (X) window key
        if cv2.getWindowProperty(self.name, 1) >= 0:  # this will send True if !(X window button) when the current window will be closed
            return True
        else:
            return False

    def __del__(self):  # close all windows
        if self.name is None:
            pass
        else:
            cv2.destroyWindow(self.name)