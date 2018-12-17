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

    def keyAct(self, key, mainWindow, autoMode, frame, soleImgPos, autoImgSave, Set):  #, frame, auto_mode
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
                mainWindow.loadDefaultSquare(frame, int(soleImgPos[0]), int(soleImgPos[1]), int(soleImgPos[2]),
                                         int(soleImgPos[3]))
            # better to make something with View draw() func
            if not autoMode:  # if auto we don't need to print "Download squar..." every time
                log.log("\'D\'" + ' ' + "Download square pos from set file", __name__)

        # save square pos (to settings)
        if key == 4:
            kok = mainWindow.returnRefPt()
            if kok != 0:
                # setting dict creation
                data = {}
                data['cam'] = [0, frame.shape[1], frame.shape[0]]  # 0, 640, 480
                data['soleImgPos'] = [kok[0][0], kok[0][1], kok[1][0], kok[1][1]]  # 45, 169, 594, 360
                data['auto'] = True if autoMode else False
                data['imgSave'] = True if autoImgSave else False

                Set.save(data)  # better return it from where you call it (controller.py) and save Set.save(data) there
                # but pressed key analysis method is here ???

                log.log("\'S\' " + "conf.set is saved", __name__)
            else:
                log.log("Nothing to save!", __name__)

        return 0