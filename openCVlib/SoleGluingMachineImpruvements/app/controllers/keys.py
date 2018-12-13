# keys controller (includes additional keys functionality)

import sys

sys.path.append('../models')
sys.path.append('../views')
from debug import Debug

log = Debug(True, __name__)  # turn on/off debugging messages in this module

class Keys:
    def __init__(self):
        self.key = -1
        # self.ReadOrSaveImg = imgRW.ImgRW()

    def keyAct(self, key, mainWindow, autoMode, frame, setStr, autoImgSave, Set):  #, frame, auto_mode
        # print(mainWindow.moveWindow(100, 100))
        # pass

        #  close window
        if key == 0:
            return 1  # isClosed

        # save highlighted square as sole pos
        if key == 2:  # ord("s") set sole pos by mouse click - crop - and unclick
            mainWindow.mousePosToZero()
            log.log("\'R\'" + ' ' + "Reset current square", __name__)

        # hide square sole pos
        if key == 3 or autoMode:  # ord("d") default square (from settings file) # autoMode (auto_on) from conf.set
            mainWindow.loadDefaultSquare(frame, int(setStr[1][0]), int(setStr[1][1]), int(setStr[1][2]),
                                         int(setStr[1][3]))

            # better to make something with View draw() func
            if not autoMode:  # if auto we don't need to print "Download squar..." every time
                log.log("\'D\'" + ' ' + "Download square pos from set file", __name__)

        if key == 4:  # save square pos (to settings)
            kok = mainWindow.returnRefPt()
            if kok != 0:
                if autoImgSave and autoMode:  # for auto mod img save according conf.set
                    tmpStr = "|auto_on|img_save_on"
                elif not autoImgSave and autoMode:
                    tmpStr = "|auto_on|img_save_off"
                else:
                    tmpStr = "|auto_off|img_save_on"

                Set.save(str(frame.shape[1]) + ',' + str(frame.shape[0]) + '|' + str(kok[0][0]) + ',' + str(
                    kok[0][1]) + ',' +
                         str(kok[1][0]) + ',' + str(kok[1][1]) + tmpStr)  # [(x1, y1), (x2, y2)])

                print("\'S\'" + ' ' + "Save square")
            else:
                print("Nothing to save!")

        return 0