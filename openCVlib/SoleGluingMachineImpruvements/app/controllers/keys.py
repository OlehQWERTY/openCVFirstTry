# keys controller (includes additional keys functionality)

import sys

sys.path.append('../models')
sys.path.append('../views')
from debug import Debug

log = Debug(True, __name__)  # turn on/off debugging messages in this module

class Keys:
    def __init__(self):
        self.key = -1
        self.flMouse = False
        # self.ReadOrSaveImg = imgRW.ImgRW()

    def flMouse(self, flag):
        self.flMouse = flag

    def keyAct(self, key, mainWindow, autoMode, frame, setStr, autoImgSave, Set):  #, frame, auto_mode
        # print(mainWindow.moveWindow(100, 100))

        #  close window
        if key == 0:
            return 1  # isClosed

        # reset highlighted square as sole pos
        if key == 2:  # ord("s") set sole pos by mouse click - crop - and unclick
            mainWindow.mousePosToZero()
            self.flMouse = False
            log.log("\'R\'" + ' ' + "Reset current square", __name__)

        # load square pos from set file
        if key == 3 or autoMode:  # ord("d") default square (from settings file) # autoMode (auto_on) from conf.set

            #!!!!!!!!!!!!!!!!Needs changes flMouse from outside according to View!!!!!!!!!!!!!!!!!!!

            if not self.flMouse:  # if image was cropped according to mouse in auto mode turn off this
                mainWindow.loadDefaultSquare(frame, int(setStr[1][0]), int(setStr[1][1]), int(setStr[1][2]),
                                         int(setStr[1][3]))
            # better to make something with View draw() func
            if not autoMode:  # if auto we don't need to print "Download squar..." every time
                log.log("\'D\'" + ' ' + "Download square pos from set file", __name__)

        # save square pos (to settings)
        if key == 4:
            kok = mainWindow.returnRefPt()
            if kok != 0:
                if autoImgSave and autoMode:  # for auto mod img save according conf.set
                    tmpStr = "|auto_on|img_save_on"
                elif not autoImgSave and autoMode:
                    tmpStr = "|auto_on|img_save_off"
                elif not autoImgSave and not autoMode:
                    tmpStr = "|auto_off|img_save_off"
                else:
                    tmpStr = "|auto_off|img_save_on"

                Set.save('0,' + str(frame.shape[1]) + ',' + str(frame.shape[0]) + '|' + str(kok[0][0]) + ',' + str(
                    kok[0][1]) + ',' +
                         str(kok[1][0]) + ',' + str(kok[1][1]) + tmpStr)  # [(x1, y1), (x2, y2)])
                log.log("\'S\' " + "Save square", __name__)
            else:
                log.log("Nothing to save!", __name__)

        return 0