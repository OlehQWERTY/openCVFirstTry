# controller for 3 models: barcode, findObj and imgRW

import sys
import time

sys.path.append('../models')
sys.path.append('../views')

from debug import Debug
import barcode
import findObj
import imgRW

log = Debug(True, __name__)  # turn on/off debugging messages in this module

# log.log("Hi", __name__)

class MachineCellAnalizer:
    def __init__(self):
        self.ReadOrSaveImg = imgRW.ImgRW()

    def processing(self, soleImg, frame, auto_mode):

        start_time = time.time()

        last_img_processing_time = time.time()  # we needs it for relay life time extention
        # log.log("Last img processing: %s" % int(last_img_processing_time), __name__)

        locTimeImgProc = time.localtime(last_img_processing_time)
        log.log("Last img processing: %s" % str(locTimeImgProc[2]) + '/' + str(locTimeImgProc[1]) + '/' \
                + str(locTimeImgProc[0]) + ' ' + str(locTimeImgProc[3]) + ':' + str(locTimeImgProc[4]) + ':' \
                + str(locTimeImgProc[5]), __name__)

        # soleImg = mainWindow.returnSoleImg()

        cor = findObj.find(soleImg)  # sole image

        # log.log('Processed sole res: %s %s' % (soleImg.shape[1], soleImg.shape[0]), __name__)

        isSoleStr = 'Sole(no points)'
        if not cor:
            pass
        else:
            if cor[0] / cor[1] > 0.2 and cor[1] > 8:  # and cor[0]/float(cor[1]) > 0.2: # check
                isSoleStr = 'NoSole' + '-' + str(cor[0]) + '-' + str(cor[1])
                log.log("cor[0]/cor[1]: " + str(cor[0]) + '/' + str(cor[1]), __name__)
            else:
                isSoleStr = 'Sole'

        barCodeData, barcodePos = self.barcodeProcessing(frame)  # barcode processing

        localTime = time.localtime(time.time())

        saveImgName = str(localTime[2]) + '-' + str(localTime[1]) + '-' \
                      + str(localTime[0]) + '-' + str(localTime[3]) + '-' + str(localTime[4]) + '-' \
                      + str(localTime[5]) + '-' + isSoleStr + '-' + 'QR' + '-' + str(barCodeData[1])  # 'IMGs/' +

        if auto_mode:  # auto save img according to conf
            self.ReadOrSaveImg.rw('W', '../IMGs/' + saveImgName + '.png', frame)  # save to img with imgName date + .png
            log.log('%s is saved' % saveImgName, __name__)
        else:
            log.log('%s' % saveImgName, __name__)
            pass

        elapsed_time = time.time() - start_time

        log.log("Iteration score: %f" % elapsed_time, __name__)

        return saveImgName, last_img_processing_time, barcodePos

    def barcodeProcessing(self, frame):
        barCodeData = barcode.zbar(frame)

        barcodePos = None
        if barCodeData is None:
            barCodeData = ['No', 'No']
        else:
            barcodePos = {'x': 0, 'y': 0, 'w': 0, 'h': 0}  # barcode pos on the picture
            i = 0
            barVar = ['x', 'y', 'w', 'h']
            for bar in barCodeData[2:]:
                barcodePos[barVar[i]] = bar
                i += 1
            # log.log(barcodePos, __name__)

        return barCodeData, barcodePos


    # def __del__(self):
    #     pass