class Settings():

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, "r") # encoding="utf8")

    def load(self):
        self.file = open(self.path, "r") # encoding="utf8")
        str1 = self.file.read()
        self.file.close()
        self.wordsObj = str1.split('|')  # split to words
        for x in range(0, len(self.wordsObj)):
            self.wordsObj[x] = self.wordsObj[x].split(',')
        return self.wordsObj

    def save(self, str):
        self.file = open(self.path, "w")
        self.file.write(str)

