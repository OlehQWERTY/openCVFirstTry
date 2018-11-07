# It is needed to divide this class to two files: view controller + universal view for any purposes
# create #1 view - main window #2 view - first additional window ...
# add callback for spec view func (additional windows needs to drow something spec so just make draw(callback) in basic obj)


import cv2
import math # sqrt()

class View:

    def __init__(self, name, w = 640, h = 480): # w h are neaded for texting resolution
        if name is None:
            print("Can't create window without name!")
        else:
            self.name = name
            cv2.namedWindow(self.name)
            if w == 640:
                # in case of vga resolution return 2 val (the same as 320*240)
                self.createTrackbar('resMode', int(math.sqrt(w/80))+1) # 640 * 480 shows 2 against 3
            else:
                self.createTrackbar('resMode', int(math.sqrt(w / 80)))  # 640 * 480 shows 2 against 3

            self.setCamW = w # change
            self.setCamH = h

            cv2.setMouseCallback(self.name, self.click_and_crop) # mouse callback

            self.kok = None


    def click_and_crop(self, event = None, x = None, y = None, flags = None, param = None): # def click_and_crop(event, x, y, flags, param):
        # grab references to the global variables
        # global refPt, cropping
        # self.refPt, self.cropping

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True

            # self.kokCrop = self.cropping  # crutch

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False
            # print(self.refPt)
            self.kok = self.refPt  # crutch
            # self.kokCrop = self.cropping # crutch

        # elif event == cv2.EVENT_MOUSEMOVE: # movement pos
        #     self.mouseMovementPos = (x, y)
        #     pass

            # print(x, y)

            # draw a rectangle around the region of interest
            # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            # cv2.imshow("image", image)

    def returnRefPt(self): # crutch for refPt available from outside
        # if self.kokCrop == False: # mouse is pressed right now
        #     return self.kok
        if self.kok is None:
            return 0
        else:
            if len(self.kok) == 2:
                return self.kok
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
            # if 'self.trackbarName' in globals(): #locals()
            self.trackbarMaxVal = maxVal
            cv2.createTrackbar(self.trackbarName, self.name, self.trackbarVal, self.trackbarMaxVal, self.resMode) # trackbar

    # def draw(self, callback): # get draw from outside ?
    #     # drawText
    #     # drawSquare
    #     pass

    def draw(self, img):

        self.show2(img)

        self.show1(img) # temp order

        self.k = cv2.waitKey(1)  # 50 # don't work without this
        return self.key() # return pressed key (ESC - exit)


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

    def show2(self, img): # addition window with squared part of main window
        # square according to mouse
        self.kokok = self.returnRefPt()
        if self.kokok != 0:
            if (self.kokok[0][0] < self.kokok[1][0]) and (self.kokok[0][1] < self.kokok[1][1]):
                self.soleImg = img[self.kokok[0][1]:self.kokok[1][1] + 1,
                      self.kokok[0][0]:self.kokok[1][0] + 1]  # +1 аби не вилітало при 0 розмірі
                cv2.resizeWindow("SoleImg", self.soleImg.shape[1],
                                 self.soleImg.shape[0])  # resize window according to web camera frame resolution
                cv2.namedWindow('SoleImg',
                                cv2.WINDOW_GUI_NORMAL)  # resize window in another way !!!!!! try cv2.GUI_EXPANDEDS
                cv2.imshow("SoleImg", self.soleImg)
                cv2.rectangle(img, (self.kokok[0][0], self.kokok[0][1]), (self.kokok[1][0] + 1, self.kokok[1][1] + 1),
                              (0, 0, 255), 2)
            else:  # _______________close soleImg window !!!!! exchange top left and bottom right points among each other
                # cv2.destroyWindow("SoleImg")  # move it somewhere else

                self.soleImg = img[self.kokok[1][1]:self.kokok[0][1] + 1, self.kokok[1][0]:self.kokok[0][0] + 1]
                cv2.resizeWindow("SoleImg", self.soleImg.shape[1],
                                 self.soleImg.shape[0])  # resize window according to web camera frame resolution
                cv2.namedWindow('SoleImg',
                                cv2.WINDOW_GUI_NORMAL)  # resize window in another way !!!!!! try cv2.GUI_EXPANDEDS
                cv2.imshow("SoleImg", self.soleImg)
                cv2.rectangle(img, (self.kokok[0][0], self.kokok[0][1]), (self.kokok[1][0] + 1, self.kokok[1][1] + 1),
                              (0, 0, 255), 2)
                # return self.soleImg
    def returnSoleImg(self): # crutch
        return self.soleImg

    def kokokToZero(self): # this func is responsible for hiding square (mouse pressed and unpressed pos)
        self.kok = None
        cv2.destroyWindow("ROI") # move it somewhere else

    def resizeImg(self, img, w = 0, h = 0):
        if w!=0 and h!=0 and w > 0 and h > 0:
            img = cv2.resize(img, (w, h))
        else:
            img = cv2.resize(img, (self.setCamW, self.setCamH))
        return img.copy()

    def key(self): # pressed key proc
        # print(self.k)
        if self.k == 27: # ESC
            return 0
        elif self.k == 32: # Space
            return 1
        # if the 's' key is pressed, break from the loop
        elif self.k == ord("s"): # del sole position on the screen
            return 2
        else:
            return 100

    def moveWindow(self, x, y): # set window pos (not used now)
        cv2.moveWindow(self.name, x, y)

    def getWindowProperty(self): # used for closing program by pressing exit (X) window key
        if cv2.getWindowProperty(self.name, 0) >= 0: # this will send True if !(X window button) when the current window will be closed
            return True
        else:
            return False

    def __del__(self): # close all windows
        if self.name is None:
            pass
        else:
            cv2.destroyWindow(self.name)
