import cv2

class ImgRW:

    def __init__(self):
        pass

    def rw(self, key='R', path=None, img=None):
        if '.png' in path or '.jpg' in path:
            if key is 'R':
                imgR = cv2.imread(path, 0)
                return imgR.copy()

            elif key is 'W':
                cv2.imwrite(path, img)
                return 1
            else:
                print("Error: Wrong key!")
        else:
            print("Error: Wrong path!")
            return 0
    #
    # def __del__(self):
    #     pass
