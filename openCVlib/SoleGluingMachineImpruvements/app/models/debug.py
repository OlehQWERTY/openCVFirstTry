class debug:
    def __init__(self, flag):
        if flag:
            print("logging started")
            self.DEBUG = True
        else:
            self.DEBUG = False

    def log(self, s):
        if self.DEBUG:  # DEBUG = True
            print(s)
            return self.DEBUG

    # log("hello world")