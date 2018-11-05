import cv2

class View:

    def __init__(self, name):
        if name is None:
            print("Can't create window without name!")
        else:
            self.name = name
            cv2.namedWindow(self.name)
        # self.max = max

    def show(self, img):
        cv2.imshow(self.name, img)
        self.k = cv2.waitKey(1)  # 50 # don't work without this
        return self.key()

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
