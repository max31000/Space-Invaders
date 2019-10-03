import json


class Json:
    def __init__(self, name):
        self.file = open(name, 'r')
        self.name = name
        self.most = json.load(self.file)['top']

    def __del__(self):
        self.file.close()
        file = open(self.name, 'w', encoding='utf-8')
        json.dump({"top": self.most}, file)
        file.close()

    def write_most(self, score):
        if self.most < score:
            self.most = score

    def read_most(self):
        return self.most
