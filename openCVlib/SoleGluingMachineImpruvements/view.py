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

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False
            # print(self.refPt)

            self.kok = self.refPt # crutch

            # draw a rectangle around the region of interest
            # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            # cv2.imshow("image", image)

    def returnRefPt(self): # crutch for refPt available from outside
        if self.kok is None:
            # pass
            return 0
        else:
            if len(self.kok) == 2:
                return self.kok
            else:
                return 0
            # pass
        # print(self.refPt)
        # if len(self.refPt) == 2:
        #     return self.refPt
        # else:
        #     return 0

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

        # square according to mouse
        ###_____________________________________________________________________________###
        self.kokok = self.returnRefPt()
        if self.kokok != 0:
            if (self.kokok[0][0] < self.kokok[1][0]) and (self.kokok[0][1] < self.kokok[1][1]):
                roi = img[self.kokok[0][1]:self.kokok[1][1], self.kokok[0][0]:self.kokok[1][0]]
                cv2.resizeWindow("ROI", roi.shape[1],
                                 roi.shape[0])  # resize window according to web camera frame resolution
                print(roi.shape)
                cv2.namedWindow('ROI', cv2.WINDOW_GUI_NORMAL) # resize window in another way !!!!!! try cv2.GUI_EXPANDEDS
                cv2.imshow("ROI", roi)
                # print("kokok 0 0 %s" % self.kokok[0][0])
                # print("kokok 0 1 %s" % self.kokok[0][1])
                cv2.rectangle(img, (self.kokok[0][0], self.kokok[0][1]), (self.kokok[1][0], self.kokok[1][1]), (0, 0, 255), 2)
            else: # _______________close roi window !!!!! exchange top left and bottom right points among each other
                # cv2.destroyWindow("ROI")  # move it somewhere else

                roi = img[self.kokok[1][1]:self.kokok[0][1], self.kokok[1][0]:self.kokok[0][0]]
                cv2.resizeWindow("ROI", roi.shape[1],
                                 roi.shape[0])  # resize window according to web camera frame resolution
                cv2.namedWindow('ROI',
                                cv2.WINDOW_GUI_NORMAL)  # resize window in another way !!!!!! try cv2.GUI_EXPANDEDS
                cv2.imshow("ROI", roi)
                # print("kokok 0 0 %s" % self.kokok[0][0])
                # print("kokok 0 1 %s" % self.kokok[0][1])
                cv2.rectangle(img, (self.kokok[0][0], self.kokok[0][1]), (self.kokok[1][0], self.kokok[1][1]),
                              (0, 0, 255), 2)
        ###_____________________________________________________________________________###

        cv2.imshow(self.name, img)
        # if self.name is 'MachineImprovements': # not universal approach (MachineImprovements should be first window)
        # cv2.putText(img, str(self.setCamW) + '*' + str(self.setCamH), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        #             (255, 255, 0), 2)
        # self.createTrackbar('resMode')


        self.k = cv2.waitKey(1)  # 50 # don't work without this
        return self.key() # return pressed key (ESC - exit)

    def kokokToZero(self): # this func is responsible for hiding square (mouse pressed and unpressed pos)
        # self.kokok = 0
        self.kok = None
        cv2.destroyWindow("ROI") # move it somewhere else

    def resize(self, img, w = 0, h = 0):
        if w!=0 and h!=0 and w > 0 and h > 0:
            imgToShow = cv2.resize(img, (w, h))
        else:
            imgToShow = cv2.resize(img, (self.setCamW, self.setCamH))
        return imgToShow.copy()

    def key(self): # pressed key proc
        # print(self.k)
        if self.k == 27: # ESC
            return 0
        elif self.k == 32: # Space
            return 1
        # if the 's' key is pressed, break from the loop
        elif self.k == ord("s"): # set sole position on the screen
            return 2
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
