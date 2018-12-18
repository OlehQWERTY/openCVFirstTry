# from debug import debug

# log = debug(True)

# log.log("koko")

# log(self.WARNING + name) or log.log(log.WARNING + name) from outside

class Debug:
    # colours for messages
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORDINARY = '\033[0m'

    def __init__(self, flag, name=None):
        if flag:
            # if name is not None:
            #     print(name, "module turn on debugging...")
            self.DEBUG = True
        else:
            self.DEBUG = False

    def log(self, s, name=None):
        if self.DEBUG:  # DEBUG = True
            if name is None:
                print(s)
            else:
                if name == "__main__":  # other colour for __main__
                    print(self.OKBLUE + name, ": " + self.ORDINARY, s)
                else:
                    print(self.WARNING + name, ": " + self.ORDINARY + s)
            return self.DEBUG
