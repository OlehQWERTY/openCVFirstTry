#  rewrite use console params and save only sole img part coordinates

# conf copy
# 0,640,480|45,169,594,360|auto_on|img_save_off

import os, sys
import pickle  # serializer/deserializer

sys.path.append('../models')
from debug import Debug
log = Debug(True, __name__)  # turn on/off debugging messages in this module

class Settings():
    def __init__(self, path):
        self.path = path
        self.data_new = None
        self.data = None

    def setPath(self, path):
        self.path = path

    def load(self):
        if self.path is not None:
            if not os.path.exists(self.path):
                print(self.path)
                log.log("Can't load file, because it doesn't exist!", __name__)
        else:
            log.log("Path is empty!", __name__)

        with open(self.path, 'rb') as f:
            self.data_new = pickle.load(f)
            return self.data_new

        return None

    def save(self, data):
        self.data = data
        with open(self.path, 'wb') as f:
            pickle.dump(data, f)
        log.log("Object was saved successfully...", __name__)

    # def parse(self):
    #     if self.data_new is not None:
    #         pass

    def __del__(self):
        log.log("Settings is closed!", __name__)


if __name__ == '__main__':  # call only if this module is called independently
    Set = Settings("test.set")

    # data = {
    #     'cam': [0, 640, 480],
    #     'soleImgPos': [45, 169, 594, 360],
    #     'auto': True,
    #     'imgSave': False,
    #     'autoImgQR': False
    # }

    # Set.save(data)
    Set.save([])  # create an empty file for dbDataProc.py save
    print(Set.load())


